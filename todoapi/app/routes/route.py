from fastapi import APIRouter, HTTPException, Request, Depends
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.crud.crud import (create_document, get_document_by_id, get_all_documents, update_document, delete_document)
from app.models.models import (CreateTaskPayload, UpdateTaskPayload, CreateUserPayload, UpdateUserPayload,UpdateTaskStatusPayload)
from app.database.db import Users_Collection, Tasks_Collection

router = APIRouter()

# Define allowed collection models for validation
CREATE_MODELS = {
    "users": CreateUserPayload,
    "tasks": CreateTaskPayload
}

UPDATE_MODELS = {
    "users": UpdateUserPayload,
    "tasks": UpdateTaskPayload
}

# Mapping collection names to actual MongoDB collections
COLLECTIONS = {
    "users": Users_Collection,
    "tasks": Tasks_Collection
}

base_dir = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(base_dir / "app/templates"))

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Create a new document (user/task)
@router.post("/{collection_name}")
async def create_item(collection_name: str, payload: CreateUserPayload | CreateTaskPayload):
    if collection_name not in CREATE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    validated_data = payload.model_dump()  # ✅ Convert Pydantic model to dictionary

    return create_document(collection_name, validated_data)


# Get a document by ID
@router.get("/{collection_name}/{item_id}")
async def get_item(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    return get_document_by_id(collection_name, item_id)


# Get all documents
@router.get("/{collection_name}")
async def get_all_items(collection_name: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    return get_all_documents(collection_name)


# Update a document by ID
@router.put("/{collection_name}/{item_id}")
async def update_item(collection_name: str, item_id: str, payload: UpdateUserPayload | UpdateTaskPayload):
    if collection_name not in UPDATE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    validated_data = payload.model_dump(exclude_unset=True)  # ✅ Convert to dict

    return update_document(collection_name, item_id, validated_data)


@router.patch("/tasks/{item_id}/update_status")
async def update_task_status(item_id: str, payload: UpdateTaskStatusPayload):
    validated_data = payload.model_dump(exclude_unset=True)
    if "status" not in validated_data:
        raise HTTPException(status_code=400, detail="Status field is required")
    return update_document("tasks", item_id, validated_data)


# Delete a document by ID
@router.delete("/{collection_name}/{item_id}")
async def delete_item(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    return delete_document(collection_name, item_id)
