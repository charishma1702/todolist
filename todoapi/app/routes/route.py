from fastapi import APIRouter, HTTPException, Request
from app.crud.crud import (create, get_by_id, get_all, update, delete)
from app.models.models import (CreateTaskPayload, UpdateTaskPayload, CreateUserPayload, UpdateUserPayload,UpdateTaskStatusPayload,CreateCategoryPayload)
from app.database.db import Users_Collection, Tasks_Collection, Categories_Collection
from bson import ObjectId

router = APIRouter()

# Define allowed collection models for validation
CREATE_MODELS = {
    "users": CreateUserPayload,
    "tasks": CreateTaskPayload,
    "categories": CreateCategoryPayload
}

UPDATE_MODELS = {
    "users": UpdateUserPayload,
    "tasks": UpdateTaskPayload,
    "categories": UpdateTaskPayload
}

# Mapping collection names to actual MongoDB collections
COLLECTIONS = {
    "users": Users_Collection,
    "tasks": Tasks_Collection,
    "categories":Categories_Collection
}


@router.post("/{collection_name}")
async def create_item(collection_name: str, request: Request, payload: CreateUserPayload | CreateTaskPayload | CreateCategoryPayload):
    if collection_name not in CREATE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    model = CREATE_MODELS[collection_name]
    if payload:
        validated_data = payload.model_dump()
    else:
        body = await request.json()
        try:
            model(**body)
            validated_data = body
        except ValueError as e:
            raise HTTPException(status_code=422, detail="Please provide valid data")
    # Call the CRUD function to create the item in the database
    return create(collection_name, validated_data)

# Get a document by ID
@router.get("/{collection_name}/{item_id}")
async def get_item(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    return get_by_id(collection_name, item_id)


# Get all documents
@router.get("/{collection_name}")
async def get_all_items(collection_name: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    return get_all(collection_name)


@router.put("/{collection_name}/{item_id}")
async def update_item(collection_name: str, item_id: str, payload: UpdateUserPayload | UpdateTaskPayload):
    if collection_name not in UPDATE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    validated_data = payload.model_dump(exclude_unset=True)  #  Convert to dict
    return update(collection_name, item_id, validated_data)


@router.patch("/tasks/{item_id}/update_status")
async def update_task_status(item_id: str, payload: UpdateTaskStatusPayload):
    validated_data = payload.model_dump(exclude_unset=True)
    if "status" not in validated_data:
        raise HTTPException(status_code=400, detail="Status field is required")
    return update("tasks", item_id, validated_data)


@router.patch("/categories/{item_id}")
async def update_category(item_id: str, payload: dict):
    validated_data = {k: v for k, v in payload.items() if v is not None}
    if not validated_data:
        raise HTTPException(status_code=400, detail="No data to update")
    return update("categories", item_id, validated_data)

# Delete a document by ID
@router.delete("/{collection_name}/{item_id}")
async def delete_item(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    return delete(collection_name, item_id)

@router.delete("/categories/{item_id}")
async def delete_category(item_id: str):
    return delete("categories", item_id)


