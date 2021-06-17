import datetime
import logging
import os
from typing import Any, Dict

import pymongo
from bson.objectid import ObjectId


def send_to_mongo(
    request_id: str,
    request_time: datetime.datetime,
    request_args: Dict[str, Any],
    request_headers: Dict[str, Any],
    request_data: Dict[str, Any],
    sent_to_discord: bool,
) -> bool:

    client: pymongo.MongoClient = pymongo.MongoClient(os.getenv("mongo_conn"))
    database: pymongo.database.Database = client.get_database(name=os.getenv("mongo_database"))
    collection: pymongo.collection.Collection = database.get_collection(name=os.getenv("mongo_collection"))

    record: Dict[str, str or datetime.datetime] = {
        "_id": ObjectId(),
        "requestId": request_id,
        "requestTime": request_time,
        "sentToDiscord": sent_to_discord,
        "requestArgs": request_args,
        "requestHeaders": request_headers,
        "requestData": request_data,
    }

    insert_id = collection.insert_one(record).inserted_id

    logging.debug(f"Request logged in MongoDb successfully with Insert ID {insert_id}")

    return True
