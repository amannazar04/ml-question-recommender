# backend/app/check_db.py
import os, asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://amannazar:87654321@cluster0.piesrhb.mongodb.net/hello?retryWrites=true&w=majority&appName=Cluster0"

DB = "hello"

async def main():
    client = AsyncIOMotorClient(MONGO_URI)
    col = client[DB]["questions"]
    count = await col.count_documents({})
    doc = await col.find_one({})
    print("Documents in collection:", count)
    print("Sample doc:", doc)

if __name__ == "__main__":
    asyncio.run(main())
