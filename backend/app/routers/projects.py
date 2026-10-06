from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_projects():
    return {"projects": []}

@router.post("")
async def create_project(data: dict):
    return {"id": 1, **data}
