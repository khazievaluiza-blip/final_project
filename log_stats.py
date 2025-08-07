from pymongo.synchronous.collection import Collection
from log_writer import connect_mongo
from colorama import Fore, Style

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
        print(f"{Fore.MAGENTA}{i}.{Style.RESET_ALL} {doc['request']} — {doc['createdAt']} ")