# backend/app/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"  # small and fast; 384-dim embeddings

class Embedder:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        Encode list[str] -> numpy array (n, d), dtype float32
        We normalize embeddings so cosine similarity == inner product.
        """
        embs = self.model.encode(list(texts), show_progress_bar=False)
        # convert to float32 and normalize
        embs = np.array(embs, dtype="float32")
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        embs = embs / norms
        return embs
