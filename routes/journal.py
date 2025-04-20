from fastapi import APIRouter, status
from pydantic import BaseModel
from modules import database

router = APIRouter()

class JournalEntryUpload(BaseModel):
    entry_id: str
    note: str

class CreateJournalEntryResponse(BaseModel):
    entry_id: str

@router.post("/journal/create_entry", response_model=CreateJournalEntryResponse, status_code=status.HTTP_200_OK)
async def create_entry(journal_entry: JournalEntryUpload):
    # TODO: Write create entry function

    return CreateJournalEntryResponse(entry_id=str(uuid4()))