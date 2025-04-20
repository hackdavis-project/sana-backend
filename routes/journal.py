import logging
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from modules import database
from uuid import uuid4
import asyncio
from modules.gemini import classify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

from typing import Optional

class JournalEntryUpload(BaseModel):
    entry_id: str
    note: Optional[str] = None
    shared: Optional[bool] = None
    classification: Optional[str] = None

class CreateJournalEntryResponse(BaseModel):
    entry_id: str

from utils.auth import get_current_user

@router.get("/journal/create_entry", response_model=CreateJournalEntryResponse, status_code=status.HTTP_200_OK)
async def create_entry(user=Depends(get_current_user)):
    logger.info(f"Creating journal entry for user_id={user['user_id']}")
    entry_id = await database.create_journal_entry(user['user_id'])
    logger.info(f"Created journal entry with entry_id={entry_id}")
    return CreateJournalEntryResponse(entry_id=entry_id)

@router.post("/journal/update_entry", status_code=status.HTTP_200_OK)
async def update_entry(journal_entry: JournalEntryUpload, user=Depends(get_current_user)):
    logger.info(f"Updating journal entry: entry_id={journal_entry.entry_id}, user_id={user['user_id']}, payload={journal_entry.dict()}")
    try:
        await database.update_journal_entry(
            entry_id=journal_entry.entry_id,
            note=journal_entry.note,
            classification=journal_entry.classification,
            shared=journal_entry.shared
        )
        if journal_entry.note:
            async def classify_and_update():
                try:
                    logger.info(f"Running Gemini classifier for entry_id={journal_entry.entry_id}")
                    result = await classify(journal_entry.note)
                    logger.info(f"Classifier result for entry_id={journal_entry.entry_id}: {result.category}")
                    await database.update_journal_entry(
                        entry_id=journal_entry.entry_id,
                        classification=result.category
                    )
                except Exception as e:
                    logger.error(f"Error in background classification for entry_id={journal_entry.entry_id}: {e}")
            asyncio.create_task(classify_and_update())
        entry = await database.get_journal_entry(journal_entry.entry_id)
        if entry and '_id' in entry:
            del entry['_id']
        logger.info(f"Returning updated journal entry: entry_id={journal_entry.entry_id}")
        return entry
    except Exception as e:
        logger.error(f"Error updating journal entry: entry_id={journal_entry.entry_id}, error={e}")
        raise

@router.get("/journal/get_entries", response_model=JournalEntryUpload, status_code=status.HTTP_200_OK)
async def get_entries(user=Depends(get_current_user)):
    # TODO: Write get entries function
    # user['user_id'] is available
    return JournalEntryUpload(entry_id=str(uuid4()), note="")