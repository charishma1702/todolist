from app.database.db import Tasks_Collection, Users_Collection
from fastapi import HTTPException
import uuid, datetime

#TASK CRUD
def task_serializer(task):
    return {
        "id": str(task["_id"]),
        "title": task["name"],
        "description": task.get("description", ""),
        "status": task.get("status", "pending"),
        "uid": task.get("uid", ""),
        "due_date": task.get("due_date", None),
        "priority_level": task.get("priority_level", None),
        "user_id": task.get("user_id", None)
    }

def create_task(payload):
    task_dict = payload.dict()
    if not payload.status:
        task_dict["status"] = "New"
    task_dict["uid"] = str(uuid.uuid4())

    try:
        result = Tasks_Collection.insert_one(task_dict)
        return {"message": "Task created successfully", "task_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_tasks():
    tasks = list(Tasks_Collection.find())
    return [task_serializer(task) for task in tasks]

def get_task_by_uid(task_uid: str):
    task = Tasks_Collection.find_one({"uid": task_uid})
    if task:
        return task_serializer(task)
    raise HTTPException(status_code=404, detail="Task not found")

def update_task(task_uid: str, payload):
    task_dict = payload.dict(exclude_unset=True)
    try:
        result = Tasks_Collection.update_one({"uid": task_uid}, {"$set": task_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_task(task_uid: str):
    try:
        result = Tasks_Collection.delete_one({"uid": task_uid})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#USER CRUD

def user_serializer(user):
    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "mobile": user.get("mobile"),
        "uid": user.get("uid"),
        "created_at": user.get("created_at")
    }

def create_user(payload):
    user_dict = payload.dict()
    user_dict["uid"] = str(uuid.uuid4())
    user_dict["created_at"] = datetime.datetime.now()

    try:
        Users_Collection.insert_one(user_dict)
        return {"message": "User created successfully", "user_uid": user_dict["uid"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_users():
    users = list(Users_Collection.find())
    return [user_serializer(user) for user in users]

def get_user_by_uid(user_uid: str):
    user = Users_Collection.find_one({"uid": user_uid})
    if user:
        return user_serializer(user)
    raise HTTPException(status_code=404, detail="User not found")

def update_user(user_uid: str, payload):
    user_dict = payload.dict(exclude_unset=True)
    
    try:
        result = Users_Collection.update_one({"uid": user_uid}, {"$set": user_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or no changes made")
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_user(user_uid: str):
    try:
        result = Users_Collection.delete_one({"uid": user_uid})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))