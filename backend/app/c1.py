import os
print("MONGO_URI env var is:", os.environ.get("MONGO_URI")[:120] + "..." if os.environ.get("MONGO_URI") else None)