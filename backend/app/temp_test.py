from embeddings import Embedder
from utils import load_or_create_index

embedder = Embedder()
index = load_or_create_index(dim=384)

q = embedder.encode(["hello"]).astype("float32")
print("Embed shape:", q.shape)
print("Index dim:", index.d)
