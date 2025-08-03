from pymongo import MongoClient, errors, DESCENDING
from datetime import datetime, UTC
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URL_READ = os.getenv("MONGODB_URL_READ")


def connect_mongo(func):
    """Декоратор для подключения к MongoDB и обработки ошибок"""
    def wrapper(*args, **kwargs):
        try:
            client = MongoClient(MONGODB_URL_READ)
            db = client["ich_edit"]
            collection = db["final_project_170225_KhazievaL"]
            result = func(collection, *args, **kwargs)
            client.close()
            return result
        except errors.ConnectionFailure:
            print("Ошибка подключения к MongoDB")
            return None
        except errors.OperationFailure:
            print("Ошибка авторизации или выполнения запроса")
            return None

    return wrapper


@connect_mongo
def write_log(collection, request_type, *args):
    doc = {
        "type": request_type,
        "request": " ".join(str(arg) for arg in args),
        "createdAt": datetime.now(UTC)
    }
    collection.insert_one(doc)


@connect_mongo
def pop_requests(collection):
    pipeline = [
        {"$group": {"_id": "$request", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    result = list(collection.aggregate(pipeline))
    for i, doc in enumerate(result, start=1):
        print(f"{i}. {doc['_id']} — {doc['count']}×")


@connect_mongo
def latest_requests(collection):
    result = collection.find().sort("createdAt", DESCENDING).limit(5)
    for i, doc in enumerate(result, start=1):
        print(f"{i}. [{doc['createdAt']}] {doc['type']} {doc['request']}")

if __name__ == '__main__':
    write_log("ddfgd", "fgfhdfgh fghfgh dfgh")