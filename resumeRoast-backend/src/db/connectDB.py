# db/mongo.py
import asyncio
from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError

MONGO_URI = "mongodb://admin:admin@mongo:27017"
DB_NAME = "resume_roast"

client: AsyncMongoClient = AsyncMongoClient(MONGO_URI)
db = client[DB_NAME]


async def test_connection():
    try:
        await client.aconnect()  # optional, but useful
        await client.server_info()  # triggers a real connection
        print("✅ Connected to MongoDB successfully")
    except PyMongoError as e:
        print(f"❌ MongoDB connection error: {e}")
