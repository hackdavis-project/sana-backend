from fastapi import APIRouter, status

router = APIRouter()

@router.post("/communities/lookup", status_code=status.HTTP_200_OK)
async def lookup_community():
    # TODO: Write lookup community function
    return