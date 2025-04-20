from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from modules import database
from uuid import uuid4

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
    await database.create_journal_entry(user['user_id'])
    return CreateJournalEntryResponse(entry_id=str(uuid4()))

@router.post("/journal/update_entry", status_code=status.HTTP_200_OK)
async def update_entry(journal_entry: JournalEntryUpload, user=Depends(get_current_user)):
    await database.update_journal_entry(
        journal_entry.entry_id,
        note=journal_entry.note,
        classification=journal_entry.classification,
        shared=journal_entry.shared
    )
    return await database.get_journal_entry(journal_entry.entry_id)

@router.get("/journal/get_entries", response_model=JournalEntryUpload, status_code=status.HTTP_200_OK)
async def get_entries(user=Depends(get_current_user)):
    # TODO: Write get entries function
    # user['user_id'] is available
    return JournalEntryUpload(entry_id=str(uuid4()), note="")