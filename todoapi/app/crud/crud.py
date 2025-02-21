from app.database.db import Users_Collection, Tasks_Collection, Categories_Collection
from bson import ObjectId
from pydantic import BaseModel
from fastapi import HTTPException
from passlib.context import CryptContext
from app.utils.utils import hash_password,create_access_token,verify_password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mapping collection names to actual MongoDB collections
COLLECTIONS = {
    "users": Users_Collection,
    "tasks": Tasks_Collection,
    "categories": Categories_Collection
}

# Generic function to create a document in a collection
def create(collection_name: str, payload: dict): 
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    collection = COLLECTIONS[collection_name]
    if collection_name=="users":
        existing_user=Users_Collection.find_one({'email':payload["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        payload["password"] = hash_password(payload["password"])
    try:
        result = collection.insert_one(payload)  
        payload["_id"] = str(result.inserted_id)
        access_token = None
        if collection_name == "users":
            access_token = create_access_token(data={"email": payload["email"]})
            
        return {"message": f"{collection_name.capitalize()} created successfully", "data": payload , "token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generic function to get a document by ID
def get_by_id(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]

    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")
        item["_id"] = str(item["_id"]) 
        return {"message": f"{collection_name.capitalize()} retrieved successfully", "data": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generic function to get all documents from a collection
def get_all(collection_name: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    collection = COLLECTIONS[collection_name]
    try:
        documents = list(collection.find({}))
        if not documents:
            raise HTTPException(status_code=404, detail=f"No {collection_name} found")
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return {"message": f"{collection_name.capitalize()} retrieved successfully", "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def update(collection_name: str, item_id: str, payload: dict):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    
    collection = COLLECTIONS[collection_name]
    try:
        update_result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": payload})

        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")

        # Fetch the updated document
        updated_item = collection.find_one({"_id": ObjectId(item_id)})
        updated_item["_id"] = str(updated_item["_id"])
        return {"message": f"{collection_name.capitalize()} updated successfully", "data": updated_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete function returns a success message or the deleted item
def delete(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    collection = COLLECTIONS[collection_name]
    try:
        result = collection.delete_one({"_id": ObjectId(item_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")

        return {"message": f"{collection_name.capitalize()} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def validate_status(cls, value):
    if value not in ["Completed", "Pending"]:
        raise ValueError("Invalid status value")
    return value

def validate_collection_name(collection_name: str) -> str:
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    return collection_name


