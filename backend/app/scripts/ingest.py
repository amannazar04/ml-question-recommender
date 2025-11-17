# backend/app/scripts/ingest.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import csv
import os
import asyncio
from pathlib import Path

from embeddings import Embedder
import faiss
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient

EMB_DIM = 384
INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index/index.faiss")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "similar_questions")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "questions.csv")

async def main():
    # load CSV
    rows = []
    with open(DATASET_PATH, newline='', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    texts = [ (r.get("title","") + " " + r.get("body","")) for r in rows ]
    ids = [ r.get("id") for r in rows ]

    embedder = Embedder()
    embs = embedder.encode(texts).astype("float32")

    # build FAISS index
    index = faiss.IndexFlatIP(EMB_DIM)
    index.add(embs)
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS index saved to {INDEX_PATH} with {index.ntotal} vectors")

    # insert into MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    col = client[DB_NAME]["questions"]

    tasks = []
    for i, r in enumerate(rows):
        doc = {
            "_id": r.get("id") or f"q{i:06d}",
            "title": r.get("title",""),
            "body": r.get("body",""),
            "tags": (r.get("tags") or "").split("|") if r.get("tags") else [],
            "embedding_id": i,
            "feedback": {"useful": 0, "not_useful": 0}
        }
        tasks.append(col.insert_one(doc))
    await asyncio.gather(*tasks)
    print("Inserted documents into MongoDB.")

if __name__ == "__main__":
    asyncio.run(main())


