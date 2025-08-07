from pymongo.synchronous.collection import Collection
from pymongo import MongoClient, errors
from datetime import datetime, UTC
from typing import Callable
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URL_READ = os.getenv("MONGODB_URL_READ")


def connect_mongo(func: Callable) -> Callable:
    """Decorator for connecting to MongoDB and handling errors"""

    def wrapper(*args):
        try:
            client = MongoClient(MONGODB_URL_READ)
            db = client["ich_edit"]
            collection = db["final_project_170225_KhazievaL"]
            result = func(*args, collection=collection)
            client.close()
            return result
        except errors.ConnectionFailure:
            print("MongoDB connection error")
            return None
        except errors.OperationFailure:
            print("Authentication or query execution error")
            return None

    return wrapper


@connect_mongo
def write_log(request_type: str, *args: str, collection: Collection) -> None:
    """
    Writes a log entry to the MongoDB collection.

    :param request_type: The type of user action.
    :param *args: Additional parameters of the request.
    :param collection: MongoDB collection object (passed from the decorator).
    """
    doc = {
        "request": f"{request_type} {" ".join(str(arg) for arg in args)}",
        "createdAt": datetime.now(UTC)
    }
    collection.insert_one(doc)

if __name__ == "__main__":
    write_log("Test", "test")