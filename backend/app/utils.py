# backend/app/utils.py
import os
import faiss
import numpy as np

INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index/index.faiss")
EMB_DIM = int(os.getenv("EMB_DIM", 384))

def load_or_create_index(dim=EMB_DIM):
    # use inner product (IP) with normalized embeddings so IP ~ cosine
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    else:
        index = faiss.IndexFlatIP(dim)
    return index

def save_index(index):
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
