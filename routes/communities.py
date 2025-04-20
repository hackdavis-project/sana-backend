from fastapi import APIRouter, status, Depends
from modules import database
from utils.auth import get_current_user

router = APIRouter()

@router.post("/communities/lookup", status_code=status.HTTP_200_OK)
async def lookup_community(category: str, user=Depends(get_current_user)):
    # Fetch all shared journal entries in the given category
    entries = await database.get_shared_journal_entries_by_category(category)
    # Remove user_id/email/name to ensure anonymity
    for entry in entries:
        entry.pop('user_id', None)
        entry.pop('email', None)
        entry.pop('name', None)
    return {"entries": entries}