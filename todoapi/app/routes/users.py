from fastapi import APIRouter
from app.models.models import CreateUserPayload, UpdateUserPayload
from app.crud.crud import create_user, get_all_users, get_user_by_uid, update_user, delete_user

router = APIRouter()

@router.post("/create")
async def create_user_route(payload: CreateUserPayload):
    return create_user(payload)

@router.get("/get-all-users")
async def get_all_users_route():
    return get_all_users()

@router.get("/get/{user_uid}")
async def get_user_route(user_uid: str):
    return get_user_by_uid(user_uid)

@router.put("/update/{user_uid}")
async def update_user_route(user_uid: str, payload: UpdateUserPayload):
    return update_user(user_uid, payload)

@router.delete("/delete/{user_uid}")
async def delete_user_route(user_uid: str):
    return delete_user(user_uid)