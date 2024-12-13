from pymongo import MongoClient


class DatabaseService:
    def __init__(self):
        config = {
            "host": "mongodb://database:27017",
            "username": "root",
            "password": "password",
        }
        self.client = MongoClient(**config)
        self.database = self.client.get_database("transaction_api")


db_service = DatabaseService()
