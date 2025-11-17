# backend/app/main.py
import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from embeddings import Embedder
from utils import load_or_create_index, save_index
from db import questions_col
from models import SearchRequest, IngestItem, Feedback

# settings
PORT = int(os.getenv("PORT", 8000))
EMB_DIM = int(os.getenv("EMB_DIM", 384))
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index/index.faiss")

app = FastAPI(title="Similar Questions Recommender")

# allow CORS from anywhere so Vercel/localhost can call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize embedder and index
embedder = Embedder()
index = load_or_create_index(dim=EMB_DIM)


@app.get("/")
async def root():
    return {"ok": True, "status": "Similar Questions Recommender API"}


@app.post("/search")
async def search(req: SearchRequest):
    # basic validation
    if not req.query or req.k <= 0:
        raise HTTPException(status_code=400, detail="Invalid query or k")

    # encode query
    q_emb = embedder.encode([req.query]).astype("float32")  # shape (1, d)

    # if index empty, return empty results
    if index.ntotal == 0:
        return {"query": req.query, "results": []}

    # clamp k to available vectors
    k = min(req.k, index.ntotal)

    # search (returns arrays shape (1, k))
    scores, ids = index.search(q_emb, k)
    ids = ids[0].tolist()
    scores = scores[0].tolist()

    results = []
    # fetch matching docs from MongoDB; exclude Mongo _id in projection
    for vid, score in zip(ids, scores):
        # faiss returns -1 when not enough vectors; skip
        if int(vid) == -1:
            continue

        # exclude MongoDB's internal _id so we don't return ObjectId
        doc = await questions_col.find_one(
            {"embedding_id": int(vid)},
            {"_id": 0}  # projection: do not return _id
        )
        if doc:
            results.append({
                "id": doc.get("id"),                      # CSV id like "q001"
                "title": doc.get("title", ""),
                "body": doc.get("body", ""),
                "tags": doc.get("tags", []),
                "score": float(score),
                "source_url": doc.get("source_url")
            })

    return {"query": req.query, "results": results}


@app.post("/ingest")
async def ingest(items: list[IngestItem]):
    """
    Ingest a list of items; compute embeddings, add to FAISS, and store in MongoDB.
    We use embedding_id aligned with index order (0..n-1).
    """
    if not items:
        raise HTTPException(status_code=400, detail="No items")

    texts = [f"{it.title} {it.body or ''}" for it in items]
    embs = embedder.encode(texts).astype("float32")

    # start index offset
    start_id = int(index.ntotal)
    index.add(embs)
    save_index(index)

    # store docs in MongoDB. Use "id" (CSV id) field, not Mongo _id
    tasks = []
    for i, it in enumerate(items):
        emb_id = start_id + i
        doc = {
            "id": it.id,
            "title": it.title,
            "body": it.body,
            "tags": it.tags or [],
            "embedding_id": int(emb_id),
            "feedback": {"useful": 0, "not_useful": 0},
            # optional: add source_url if your IngestItem has it
        }
        tasks.append(questions_col.insert_one(doc))

    await asyncio.gather(*tasks)
    return {"added": len(items), "start_embedding_id": start_id}


@app.post("/feedback")
async def feedback(f: Feedback):
    """
    Record user feedback. Use the CSV 'id' field to find questions.
    """
    field = "feedback.useful" if f.useful else "feedback.not_useful"
    # find by CSV id (not Mongo _id)
    await questions_col.update_one({"id": f.question_id}, {"$inc": {field: 1}})
    return {"ok": True}
