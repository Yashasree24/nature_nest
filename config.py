from pymongo import MongoClient

# MongoDB Connection URI
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "nature_nest"

# Establish connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]