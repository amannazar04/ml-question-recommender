import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


import os
import csv
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from embeddings import Embedder
import faiss
import numpy as np

# === Environment Variables ===
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB", "hello")
FAISS_INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "faiss_index/index.faiss")
EMB_DIM = int(os.environ.get("EMB_DIM", "384"))

DATASET_PATH = "dataset/questions.csv"  # CSV dataset path

# Ensure FAISS folder exists
os.makedirs("faiss_index", exist_ok=True)

embedder = Embedder()  # Uses your sentence-transformers embedding class


async def main():
    print(f"[INFO] Loading CSV dataset from: {DATASET_PATH}")

    rows = []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    print(f"[INFO] Loaded {len(rows)} rows.")

    # Prepare texts for embedding
    texts = [f"{r['title']} {r['body']}" for r in rows]

    print("[INFO] Generating embeddings...")
    embeddings = embedder.encode(texts)
    embeddings = embeddings.astype("float32")

    print("[INFO] Creating FAISS index...")
    index = faiss.IndexFlatL2(EMB_DIM)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"[INFO] FAISS index saved to {FAISS_INDEX_PATH}")

    # Connect to MongoDB
    print("[INFO] Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    col = client[MONGO_DB]["questions"]

    print("[INFO] Clearing old database entries...")
    await col.delete_many({})

    print("[INFO] Inserting rows into MongoDB...")

    tasks = []
    for i, r in enumerate(rows):
        doc = {
            "id": r["id"],
            "title": r["title"],
            "body": r["body"],
            "tags": eval(r["tags"]),  # convert "['a','b']" string into list
            "source_url": r["source_url"],
            "embedding_id": i
        }
        tasks.append(col.insert_one(doc))

    await asyncio.gather(*tasks)

    print("[SUCCESS] Ingestion completed!")
    print(f"[SUCCESS] Inserted {len(rows)} documents into DB '{MONGO_DB}'.")
    print("[SUCCESS] New FAISS index ready.")


if __name__ == "__main__":
    asyncio.run(main())
