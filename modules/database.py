from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
from uuid import uuid4
import time
import os

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))

database = client[os.getenv("DATABASE_NAME")]


async def create_mock_user() -> str:
    user_id = str(uuid4())
    document = {
        "user_id": user_id,
        "google_id": user_id,
        "email": "johnsmith" + user_id + "@gmail.com",
        "name": "John Smith",
        "preferences": {},
        "voice_id": None,
        "onboarded": False,
        "created_at": time.time(),
        "updated_at": time.time(),
    }
    await database["Users"].insert_one(document)
    return user_id


async def get_user_by_google_id(google_id: str) -> dict | None:
    return await database["Users"].find_one({"google_id": google_id})


async def get_user_by_id(user_id: str) -> dict | None:
    return await database["Users"].find_one({"user_id": user_id})


async def create_user_with_google(google_id: str, email: str, name: str) -> str:
    user_id = str(uuid4())
    document = {
        "user_id": user_id,
        "google_id": google_id,
        "email": email,
        "name": name,
        "preferences": {},
        "voice_id": None,
        "onboarded": False,
        "created_at": time.time(),
        "updated_at": time.time(),
    }
    await database["Users"].insert_one(document)
    return user_id


async def create_journal_entry(user_id: str) -> str:
    entry_id = str(uuid4())

    document = {
        "entry_id": entry_id,
        "user_id": user_id,
        "title": "",
        "note": "",
        "classification": "",
        "shared": False,
        "created_at": time.time(),
        "updated_at": time.time(),
    }

    await database["Journals"].insert_one(document)
    return entry_id


async def update_journal_entry(
    entry_id: str,
    note: str = None,
    classification: str = None,
    shared: bool = None,
    title: str = None,
) -> None:
    update_fields = {"updated_at": time.time()}
    if note not in (None, ""):
        update_fields["note"] = note
    if classification not in (None, ""):
        update_fields["classification"] = classification
    if shared is not None:
        update_fields["shared"] = shared
    if title not in (None, ""):
        update_fields["title"] = title
    await database["Journals"].update_one(
        {"entry_id": entry_id}, {"$set": update_fields}
    )


async def get_journal_entry(entry_id: str) -> dict | None:
    return await database["Journals"].find_one({"entry_id": entry_id})


async def get_all_journal_entries(user_id: str) -> list[dict]:
    return (
        await database["Journals"]
        .find({"user_id": user_id})
        .sort("updated_at", -1)
        .to_list(1000)
    )


async def get_shared_journal_entries_by_category(category: str) -> list[dict]:
    # Only return entries that are shared and match the classification/category
    return (
        await database["Journals"]
        .find({"shared": True, "classification": category})
        .sort("updated_at", -1)
        .to_list(1000)
    )


async def delete_journal_entry(entry_id: str) -> None:
    await database["Journals"].delete_one({"entry_id": entry_id})


async def add_resource(resource: dict) -> None:
    await database["Resources"].insert_one(resource)


async def get_resources() -> list[dict]:
    return await database["Resources"].find().to_list()


async def save_voice_id(user_id: str, voice_id: str) -> None:
    await database["Users"].update_one(
        {"user_id": user_id}, {"$set": {"voice_id": voice_id}}
    )


async def get_voice_id(user_id: str) -> str | None:
    user = await database["Users"].find_one({"user_id": user_id})
    return user.get("voice_id")


async def update_onboarded_status(user_id: str, onboarded: bool) -> None:
    await database["Users"].update_one(
        {"user_id": user_id}, {"$set": {"onboarded": onboarded}}
    )
