from pymongo import MongoClient
# Establish a connection to the database
client = MongoClient("mongodb://localhost:27017/")
db = client["users"]
Users_Collection = db.get_collection("users")
Tasks_Collection = db.get_collection("tasks")
Categories_Collection=db.get_collection("categories")