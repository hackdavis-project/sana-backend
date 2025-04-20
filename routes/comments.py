from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from modules.comments import add_comment, get_comments, add_reaction, get_reactions
from utils.auth import get_current_user

router = APIRouter()

class CommentRequest(BaseModel):
    entry_id: str
    text: str

class CommentResponse(BaseModel):
    comment_id: str

class ReactionRequest(BaseModel):
    entry_id: str
    emoji: str

@router.post("/comments/add", response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def add_comment_endpoint(request: CommentRequest, user=Depends(get_current_user)):
    comment_id = await add_comment(request.entry_id, user['user_id'], request.text)
    return CommentResponse(comment_id=comment_id)

@router.get("/comments/{entry_id}", status_code=status.HTTP_200_OK)
async def get_comments_endpoint(entry_id: str, user=Depends(get_current_user)):
    comments = await get_comments(entry_id)
    # Remove user_id from comments for anonymity
    for comment in comments:
        comment.pop('user_id', None)
    return {"comments": comments}

@router.post("/comments/react", status_code=status.HTTP_200_OK)
async def add_reaction_endpoint(request: ReactionRequest, user=Depends(get_current_user)):
    await add_reaction(request.entry_id, request.emoji)
    return {"status": "ok"}

@router.get("/comments/{entry_id}/reactions", status_code=status.HTTP_200_OK)
async def get_reactions_endpoint(entry_id: str, user=Depends(get_current_user)):
    reactions = await get_reactions(entry_id)
    return {"reactions": reactions}
