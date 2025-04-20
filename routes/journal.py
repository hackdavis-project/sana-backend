from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from modules import database
from uuid import uuid4

router = APIRouter()

class JournalEntryUpload(BaseModel):
    entry_id: str
    note: str

class CreateJournalEntryResponse(BaseModel):
    entry_id: str

from utils.auth import get_current_user

@router.post("/journal/create_entry", response_model=CreateJournalEntryResponse, status_code=status.HTTP_200_OK)
async def create_entry(journal_entry: JournalEntryUpload, user=Depends(get_current_user)):
    # TODO: Write create entry function
    # user['user_id'] is available
    return CreateJournalEntryResponse(entry_id=str(uuid4()))


@router.get("/journal/get_entries", response_model=JournalEntryUpload, status_code=status.HTTP_200_OK)
async def get_entries(user=Depends(get_current_user)):
    # TODO: Write get entries function
    # user['user_id'] is available
    return JournalEntryUpload(entry_id=str(uuid4()), note="")