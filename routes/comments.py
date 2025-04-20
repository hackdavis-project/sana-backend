import logging
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from modules.comments import add_comment, get_comments, add_reaction, get_reactions
from utils.auth import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(f"Adding comment: entry_id={request.entry_id}, user_id={user['user_id']}, text={request.text}")
    try:
        comment_id = await add_comment(request.entry_id, user['user_id'], request.text)
        logger.info(f"Comment added: comment_id={comment_id} for entry_id={request.entry_id}")
        return CommentResponse(comment_id=comment_id)
    except Exception as e:
        logger.error(f"Error adding comment: entry_id={request.entry_id}, error={e}")
        raise

@router.get("/comments/{entry_id}", status_code=status.HTTP_200_OK)
async def get_comments_endpoint(entry_id: str, user=Depends(get_current_user)):
    logger.info(f"Retrieving comments for entry_id={entry_id}")
    try:
        comments = await get_comments(entry_id)
        # Remove user_id from comments for anonymity
        for comment in comments:
            comment.pop('user_id', None)
        logger.info(f"Returning {len(comments)} comments for entry_id={entry_id}")
        return {"comments": comments}
    except Exception as e:
        logger.error(f"Error retrieving comments for entry_id={entry_id}: {e}")
        raise

@router.post("/comments/react", status_code=status.HTTP_200_OK)
async def add_reaction_endpoint(request: ReactionRequest, user=Depends(get_current_user)):
    logger.info(f"Adding reaction: entry_id={request.entry_id}, emoji={request.emoji}, user_id={user['user_id']}")
    try:
        await add_reaction(request.entry_id, request.emoji)
        logger.info(f"Reaction '{request.emoji}' added to entry_id={request.entry_id}")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error adding reaction: entry_id={request.entry_id}, emoji={request.emoji}, error={e}")
        raise

@router.get("/comments/{entry_id}/reactions", status_code=status.HTTP_200_OK)
async def get_reactions_endpoint(entry_id: str, user=Depends(get_current_user)):
    logger.info(f"Retrieving reactions for entry_id={entry_id}")
    try:
        reactions = await get_reactions(entry_id)
        logger.info(f"Returning reactions for entry_id={entry_id}: {reactions}")
        return {"reactions": reactions}
    except Exception as e:
        logger.error(f"Error retrieving reactions for entry_id={entry_id}: {e}")
        raise
