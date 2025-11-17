# backend/app/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://amannazar:87654321@cluster0.piesrhb.mongodb.net/?appName=Cluster0"
DB_NAME = os.getenv("MONGO_DB", "similar_questions")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
questions_col = db["questions"]
#mongo_uri mongodb+srv://amannazar:87654321@cluster0.piesrhb.mongodb.net/
#mongodb+srv://amannazar:87654321@cluster0.piesrhb.mongodb.net/

