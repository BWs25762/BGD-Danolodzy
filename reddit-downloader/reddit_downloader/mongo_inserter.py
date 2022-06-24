from typing import Literal
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError

CONNECTION_STRING = "mongodb://127.0.0.1:27017/"

class MongoInserter():

    def __init__(self) -> None:
        self.client = MongoClient(CONNECTION_STRING, username="admin", password="p@ssw0rd")
        self.db = self.client["reddit"]
        self.collection = self.db["submissions"]
    
    def set_collection(self, collection):
        self.collection = self.db[collection + "s"]

    def insert_one(self, document: dict):
        keys = document.keys()
        if "_id" not in keys and "id" in keys:
            document["_id"] = document["id"]
        try:
            self.collection.insert_one(document)
        except DuplicateKeyError:
            pass