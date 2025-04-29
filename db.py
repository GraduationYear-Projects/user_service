from pymongo import MongoClient

# Setup MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Cloud"] 