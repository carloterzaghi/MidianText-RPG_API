from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["MidiaText"]
usuarios_collection = db["usuarios"]
