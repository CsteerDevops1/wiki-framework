from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from collections import OrderedDict
import json
from datetime import datetime

import os
from dotenv import load_dotenv
# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()
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


def client_availabe(client) -> bool:
    ans = True
    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        ans = False
    return ans


def set_modification(**changes) -> dict:
    '''
    changes : <key> : <values>
    changes - changes which should be applied on document
    returns modification dict for update function
    '''
    return {"$set" : changes}


def insert(collection, data : dict):
    ''' on success returns ObjecId of inserted object '''
    result = collection.insert(data)
    return result.inserted_id


def delete(collection, filter : dict) -> int:
    ''' returns amount of deleted objects '''
    result = collection.delete_many(filter)
    return result.deleted_count


def update(collection, modification, *filters) -> int:
    ''' returns amount of modificated documents '''
    assert len(filters) != 0
    result = collection.update_many(update=modification, array_filters=filters)
    return result.modified_count


def find(collection, filter : dict = None, projection : list = None) -> list:
    '''
    filter : an object specifying elements which must be present for a document
    to be included in the result set, if None - returns whole collection
    projection (optional) : a list of field names that should be returned in the result set

    returns a list of documents
    '''
    return list(collection.find(filter, projection=projection))


if __name__ == "__main__":
    client = init_db_client()
    assert client_availabe(client)

    db = client.test_database

    # drop collection if it exists
    db.test_collection.drop()
    db.create_collection("test_collection")
    collection = client.test_database.test_collection

    set_validation(db, "test_collection", "schema.json")

    print("Print whole collection")
    print(find(collection))

    print("Inserting")
    print(insert(collection, val_post))

    print("Find inserted obj")
    print(find(collection, {"name" : "val_post1"}))

    print("Update inserted obj")
    print(update(collection, set_modification(name="updated_post1"), {"name" : "val_post1"}))

    print("Find wrong obj")
    print(find(collection, {"name" : "val_post1"}))

    print("Find correct obj, get name")
    print(find(collection, {"name" : "updated_post1"}, ["name"]))

    print("Delete wrong obj")
    print(delete(collection, {"name" : "wrong_name"}))

    print("Delete correct obj")
    print(delete(collection, {"name" : "updated_post1"}))

    print("Print whole collection")
    print(find(collection))
