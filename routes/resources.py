from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class ResourcesResponse(BaseModel):
    resources: list[dict]

@router.post("/resources/get", response_model=ResourcesResponse, status_code=status.HTTP_200_OK)
async def get_resources():
    # TODO: Write get resources function
    return ResourcesResponse(resources=[])