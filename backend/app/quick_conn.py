# quick_conn.py
import os
from pymongo import MongoClient
uri = os.environ.get("MONGO_URI")
print("Trying URI:", uri and (uri[:80] + "..." if len(uri) > 80 else uri))
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
try:
    info = client.server_info()   # will throw if cannot connect
    print("Connected to MongoDB, version:", info.get("version"))
except Exception as e:
    print("Connection failed:", type(e).__name__, e)
