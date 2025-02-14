from app.database.db import Users_Collection, Tasks_Collection, Categories_Collection
from bson import ObjectId
from fastapi import HTTPException


# Mapping collection names to actual MongoDB collections
COLLECTIONS = {
    "users": Users_Collection,
    "tasks": Tasks_Collection,
    "categories": Categories_Collection
}

# Generic function to create a document in a collection
def create(collection_name: str, payload: dict):  # ✅ Accept dict directly
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]
    
    try:
        result = collection.insert_one(payload)  # ✅ No need to convert it again
        payload["_id"] = str(result.inserted_id)
        return {"message": f"{collection_name.capitalize()} created successfully", "data": payload}
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


# Generic function to update a document by ID
def update(collection_name: str, item_id: str, payload: dict):  # ✅ Accept dict directly
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")
    
    collection = COLLECTIONS[collection_name]
    try:
        update_result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": payload})  # ✅ No dict conversion needed

        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")

        return {"message": f"{collection_name.capitalize()} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Generic function to delete a document by ID
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



