from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.database.db import Users_Collection
from fastapi import APIRouter, HTTPException
import datetime, uuid

router = APIRouter()

class CreateUserPayload(BaseModel):
    name: str
    email: str
    mobile: str

@router.post("/create/{user_uid}")
def create_user(payload: CreateUserPayload):
    user_dict = payload.dict()
    user_dict['uid'] = str(uuid.uuid4())
    user_dict['created_at'] = datetime.datetime.now()
    try:
        Users_Collection.insert_one(user_dict)
        print(user_dict['uid'])
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-all-users")
def get_all_users():
    users = list(Users_Collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return {"users": users}


@router.get("/get/{user_uid}")
def view_user(user_uid: str):
    user = Users_Collection.find_one({"uid": user_uid})
    if user:
        user_id = str(user.get("_id"))
        return {"user_id": user_id, "name": user.get("name"), "email": user.get("email"),"uid":user.get("uid")}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/put/{user_uid}")
def update_user(user_uid: str, payload: CreateUserPayload):
    user_dict = payload.dict()
    try:
        Users_Collection.update_one({"uid": user_uid}, {"$set": user_dict})
        return {"message": "User  updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{user_uid}")
def delete_user(user_uid: str):
    try:
        Users_Collection.delete_one({"uid": user_uid})
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))