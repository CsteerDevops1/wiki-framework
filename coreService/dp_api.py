from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from collections import OrderedDict
import json
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv() # doesn't override any env variables, just set them from .env file if they don't exist
MONGO_URI = os.getenv("MONGO_URI")


# wiki page example for testing
val_post = { 
            "name" : "val_post1",
            "description" : "val_post1",
            "tags" : [],
            "text" : "text",
            "creation_date" : datetime.utcnow(),
            "synonyms" : [],
            "relations" : [],
            "attachments" : [{"content_type" : "img/png", "content" : b"sdfsdf"}]
            }

def init_db_client() -> MongoClient:
    client = MongoClient(MONGO_URI)
    return client

def set_validation(db, collection_name : str, schema_path : str):
    assert collection_name in db.list_collection_names()
    command = json.dumps({"collMod" : collection_name, "validator" : {}})
    command = json.loads(command)

    with open(schema_path, 'r') as schema_file:
        schema = json.loads(schema_file.read())
    command["validator"] = schema

    db.command(OrderedDict(command))

def client_availabe(client):
    ans = True
    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        ans = False
    return ans

if __name__ == "__main__":
    client = init_db_client()
    assert client_availabe(client)

    db = client.test_database
    
    # drop collection if it exists
    db.test_collection.drop()
    db.create_collection("test_collection")
    collection = client.test_database.test_collection

    set_validation(db, "test_collection", "schema.json")

    collection.insert(val_post)
