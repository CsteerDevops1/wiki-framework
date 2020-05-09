from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, WriteError, CollectionInvalid 
from collections import OrderedDict
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import base64
import re


# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
SCHEMA_PATH = os.getenv('SCHEMA_PATH')


def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')


def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))


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

    
    def _deserialize(self, obj : dict):
        '''
        converts all the nessesary fields in given obj to
        types, which can be understood by database

        changes obj in place!
        '''
        if obj is None: return
        if "_id" in obj:
            try:
                obj["_id"] = ObjectId(obj["_id"])
            except :
                del obj["_id"]
        if "attachments" in obj:
            for item in obj["attachments"]:
                if type(item["content_data"]) == type(""):
                    item["content_data"] = bytes_from_str(item["content_data"])
        if "creation_date" in obj:
            if type(obj["creation_date"]) == type(""):
                obj["creation_date"] = datetime.fromisoformat(obj["creation_date"])


    def _serialize(self, obj : dict):
        '''
        converts all the nessesary fields in given obj to
        types, which can be understood by json

        changes obj in place!
        '''
        if obj is None: return
        if "_id" in obj:
            obj["_id"] = str(obj["_id"])
        if "creation_date" in obj:
            obj["creation_date"] = str(obj["creation_date"])
        if "attachments" in obj:
            for item in obj["attachments"]:
                if type(item["content_data"]) == type(b""):
                    item["content_data"] = bytes_to_str(item["content_data"])


    def get(self, filter : dict = None, projection : list = None, regex : bool = False) -> list:
        '''
        filter : an object specifying elements which must be present for a document
        to be included in the result set, if None - returns whole collection

        projection (optional) : a list of field names that should be returned in the result set

        regex (optional, default is False) : flag which determines whether to use regular
        expressions in search query, search is case insensitive. Wrong patterns are ignored.

        returns a list of documents
        '''
        self._deserialize(filter)
        if regex:
            for key in list(filter.keys()):
                try: # use try in case of invalid regex pattern
                    filter[key] = re.compile(filter[key], re.IGNORECASE)
                except:
                    print(f"Regex error with '{filter[key]}', can't compile")
                    del filter[key]
        result = list(self.collection.find(filter, projection=projection))
        # serialize db results
        for item in result:
            self._serialize(item)
        return result

    def create(self, data : dict) -> dict:
        ''' 
        on success returns created object,
        if fails returns None
        '''
        try:
            data["creation_date"] = datetime.utcnow()
            self._deserialize(data)
            result = self.collection.insert_one(data)
            self._serialize(data)
            return data
        except WriteError:
            return None

    def update(self, modification : dict, filter : dict) -> int:
        ''' returns amount of modificated documents '''
        self._deserialize(filter)
        self._deserialize(modification["$set"])
        result = self.collection.update_many(update=modification, filter=filter)
        return result.modified_count

    def delete(self, filter : dict) -> int:
        ''' returns amount of deleted objects '''
        self._deserialize(filter)
        result = self.collection.delete_many(filter)
        return result.deleted_count


if __name__ == "__main__":
    # wiki page example for testing
    val_post = {
            "name" : "val_post1",
            "russian_name" : "",
            "description" : "val_post1",
            "russian_description" : "",
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

    print("Find correct obj, get name, attachments")
    print(DAO_obj.get({"name" : "updated_post1"}, ["name", "attachments"]))

    print("Updating attachments")
    new_item = {
        "content_type" : "image/jpeg",
        "content_data" : "AAAAAAAA",
        "description" : "title"
    }
    print(DAO_obj.update(set_modification({"attachments" : [new_item]}), {"name" : "updated_post1"}))

    print("Find correct obj, get name, attachments")
    print(DAO_obj.get({"name" : "updated_post1"}, ["name", "attachments"]))

    print("Delete wrong obj")
    print(DAO_obj.delete({"name" : "wrong_name"}))

    print("Delete correct obj")
    print(DAO_obj.delete({"name" : "updated_post1"}))

    print("Print whole collection")
    print(DAO_obj.get())
