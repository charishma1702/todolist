from fastapi import APIRouter
from app.models.models import CreateTaskPayload, UpdateTaskPayload
from app.crud.crud import create_task, get_all_tasks, get_task_by_uid, update_task, delete_task

router = APIRouter()

@router.post("/create")
async def create_task_route(payload: CreateTaskPayload):
    return create_task(payload)

@router.get("/all")
async def get_all_tasks_route():
    return get_all_tasks()

@router.get("/{task_uid}")
async def get_task_route(task_uid: str):
    return get_task_by_uid(task_uid)

@router.put("/{task_uid}")
async def update_task_route(task_uid: str, payload: UpdateTaskPayload):
    return update_task(task_uid, payload)

@router.delete("/{task_uid}")
async def delete_task_route(task_uid: str):
    return delete_task(task_uid)