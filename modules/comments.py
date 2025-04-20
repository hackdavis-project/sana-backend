from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
import time
import os

client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
database = client[os.getenv('DATABASE_NAME')]

# Comment schema: {
#   comment_id: str,
#   entry_id: str,  # The journal entry this comment is for
#   user_id: str,   # Who commented (can be anonymized)
#   text: str,
#   created_at: float
# }

async def add_comment(entry_id: str, user_id: str, text: str) -> str:
    comment_id = str(uuid4())
    document = {
        "comment_id": comment_id,
        "entry_id": entry_id,
        "user_id": user_id,
        "text": text,
        "created_at": time.time()
    }
    await database["Comments"].insert_one(document)
    return comment_id

async def get_comments(entry_id: str) -> list[dict]:
    return await database["Comments"].find({"entry_id": entry_id}).to_list(1000)

# Emoji reactions are stored as a dict: { "emoji": count, ... }
# Each shared entry will have a reactions field, e.g. { "❤️": 3, "👏": 1 }
async def add_reaction(entry_id: str, emoji: str) -> None:
    await database["Journals"].update_one(
        {"entry_id": entry_id},
        {"$inc": {f"reactions.{emoji}": 1}}
    )

async def get_reactions(entry_id: str) -> dict:
    entry = await database["Journals"].find_one({"entry_id": entry_id})
    return entry.get("reactions", {}) if entry else {}
