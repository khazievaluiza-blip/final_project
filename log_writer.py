from pymongo.synchronous.collection import Collection
from pymongo import MongoClient, errors, DESCENDING
from datetime import datetime, UTC
from colorama import Fore, Style
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




@connect_mongo
def pop_requests(collection: Collection) -> None:
    """
    The function displays the 5 most frequent search queries stored in the MongoDB collection
    and their number. This function uses an aggregation pipeline with `$sortByCount` to group and
    sort the requests by frequency in descending order.
    :param collection: The MongoDB collection object provided by the `connect_mongo` decorator.
    """
    result = collection.aggregate([
        {
            '$sortByCount': '$request'
        }, {
            '$limit': 5
        }
    ])
    for i, doc in enumerate(result, start=1):
        print(f"{Fore.MAGENTA}{i}.{Style.RESET_ALL} {doc['_id']} — {Fore.MAGENTA}{doc['count']}{Style.RESET_ALL} times")




@connect_mongo
def latest_requests(collection: Collection) -> None:
    """
    The function displays the 5 most recent search requests stored in the MongoDB collection.
    This function connects to the MongoDB collection using the `connect_mongo` decorator,
    sorts the documents by the `createdAt` field in descending order.

    :param collection: The MongoDB collection object provided by the `connect_mongo` decorator.
    """
    result = collection.find().sort("createdAt", -1).limit(5)
    for i, doc in enumerate(result, start=1):
        print(f"{Fore.MAGENTA}{i}.{Style.RESET_ALL} {doc['request']}")



