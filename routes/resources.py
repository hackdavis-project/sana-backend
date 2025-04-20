from fastapi import APIRouter, status
from pydantic import BaseModel
from modules.gemini import find_resources

router = APIRouter()

class ResourcesResponse(BaseModel):
    resources: list[dict]

class ResourceRequest(BaseModel):
    journal_entry: str


@router.post("/resources/get", response_model=ResourcesResponse, status_code=status.HTTP_200_OK)
async def get_resources(request: ResourceRequest):
    resources_obj = await find_resources(request.journal_entry)
    return ResourcesResponse(resources=resources_obj.resources)