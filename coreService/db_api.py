from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, WriteError, CollectionInvalid 
from collections import OrderedDict
import json
from datetime import datetime
import os
from dotenv import load_dotenv


# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
SCHEMA_PATH = os.getenv('SCHEMA_PATH')


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


def set_modification(changes : dict) -> dict:
    '''
    changes : <key> : <values>
    changes - changes which should be applied on document
    returns modification dict for update function
    '''
    return {"$set" : changes}


class WikiPageDAO:
    def __init__(self):
        self.db_client = init_db_client()
        self.database = self.db_client.wikiDB
        try:
            self.database.create_collection("wikipage_collection")
            self.collection = self.database.wikipage_collection
        except CollectionInvalid: # means that collection exists
            self.collection = self.database.wikipage_collection
        set_validation(self.database, "wikipage_collection", SCHEMA_PATH)
        assert client_availabe(self.db_client) # raise error if can't conenct to db


    def get(self, filter : dict = None, projection : list = None) -> list:
        '''
        filter : an object specifying elements which must be present for a document
        to be included in the result set, if None - returns whole collection
        projection (optional) : a list of field names that should be returned in the result set

        returns a list of documents
        '''
        result = list(self.collection.find(filter, projection=projection))
        return result

    def create(self, data : dict):
        ''' 
        on success returns ObjecId of inserted object,
        if fails returns -1 
        '''
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except WriteError:
            return -1

    def update(self, modification : dict, filter : dict) -> int:
        ''' returns amount of modificated documents '''
        result = self.collection.update_many(update=modification, filter=filter)
        return result.modified_count

    def delete(self, filter : dict) -> int:
        ''' returns amount of deleted objects '''
        result = self.collection.delete_many(filter)
        return result.deleted_count


if __name__ == "__main__":
    # wiki page example for testing
    val_post = {
            "name" : "val_post1",
            "description" : "val_post1",
            "tags" : [],
            "text" : "text",
            "creation_date" : datetime.utcnow(),
            "synonyms" : [],
            "relations" : [],
            "attachments" : [{"content_type" : "image/png", "content_data" : b"sdfsdf"}]
            }

    DAO_obj = WikiPageDAO()

    print("Print whole collection")
    print(DAO_obj.get())

    print("Inserting")
    print(DAO_obj.create(val_post))

    print("Find inserted obj")
    print(DAO_obj.get({"name" : "val_post1"}))

    print("Update inserted obj")
    print(DAO_obj.update(set_modification({"name" : "updated_post1"}), {"name" : "val_post1"}))

    print("Find wrong obj")
    print(DAO_obj.get({"name" : "val_post1"}))

    print("Find correct obj, get name")
    print(DAO_obj.get({"name" : "updated_post1"}, ["name"]))

    print("Delete wrong obj")
    print(DAO_obj.delete({"name" : "wrong_name"}))

    print("Delete correct obj")
    print(DAO_obj.delete({"name" : "updated_post1"}))

    print("Print whole collection")
    print(DAO_obj.get())
