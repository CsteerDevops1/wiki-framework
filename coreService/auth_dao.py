from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, WriteError, CollectionInvalid
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
import secrets
from datetime import datetime
from time import sleep


# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
ROLES = ["ADMIN", "USER", "MODERATOR"] # possible values for role
PERMISSIONS = {
    "ADMIN" : ["create", "delete", "edit", "view"],
    "USER" : ["view"],
    "MODERATOR" : ["edit", "view"],
}
ROLE_TTL = 60 * 60 * 24 * 3 # time for role life in seconds


def init_db_client() -> MongoClient:
    client = MongoClient(MONGO_URI)
    return client

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

def generate_user_token():
    return secrets.token_hex(16)


class CRUD:
    '''
        implements basic CRUD operations to mongodb collection
    '''
    def __init__(self, collection):
        self.collection = collection

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
        if "creation_date" in obj:
            if type(obj["creation_date"]) == type(""):
                obj["creation_date"] = datetime.fromisoformat(obj["creation_date"])
        for key, value in list(obj.items()):
            if value is None:
                del obj[key]


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
        if "user_id" in obj:
            obj["user_id"] = str(obj["user_id"])

    def create(self, data : dict) -> dict:
        ''' 
        on success returns created object,
        if fails returns None
        '''
        self._deserialize(data)
        try:
            result = self.collection.insert_one(data)
            self._serialize(data)
            return data
        except WriteError:
            return None

    def update(self, modification : dict, filter : dict) -> int:
        ''' returns amount of modificated documents '''
        self._deserialize(filter)
        self._deserialize(modification.get("$set", None))
        result = self.collection.update_many(update=modification, filter=filter)
        return result.modified_count

    def delete(self, filter : dict) -> int:
        ''' returns amount of deleted objects '''
        self._deserialize(filter)
        result = self.collection.delete_many(filter)
        return result.deleted_count

    def get(self, filter : dict = None, projection : list = None) -> list:
        '''
        filter : an object specifying elements which must be present for a document
        to be included in the result set, if None - returns whole collection

        projection (optional) : a list of field names that should be returned in the result set

        returns a list of documents
        '''
        self._deserialize(filter)
        result = list(self.collection.find(filter, projection=projection))
        for item in result:
            self._serialize(item)
        return result

    def exist(self, obj_id : str) -> bool:
        res = len(list(self.collection.find({"_id" : ObjectId(obj_id)})))
        return res == 1


class WikiAuthDAO:
    def __init__(self):
        self.db_client = init_db_client()
        self.database = self.db_client.wikiDB
        try:
            self.database.create_collection("wiki_users_collection")
            self.users_collection = self.database.wiki_users_collection
        except CollectionInvalid: # means that collection exists
            self.users_collection = self.database.wiki_users_collection

        try:
            self.database.create_collection("wiki_roles_collection")
            self.roles_collection = self.database.wiki_roles_collection
        except CollectionInvalid:
            self.roles_collection = self.database.wiki_roles_collection

        assert client_availabe(self.db_client) # raise error if can't conenct to db

        self.roles_collection.create_index("creation_date", expireAfterSeconds=ROLE_TTL )

        self.roles = CRUD(self.roles_collection)
        self.users = CRUD(self.users_collection)

    def set_user_role(self, role_name : str, user_id : str):
        '''
            set user's role property to role_name, 
            won't work unless role object created in wiki_roles_collection
        '''
        global ROLES
        if user_id is None or role_name is None:
            return None
        role_name = role_name.upper()
        if not role_name in ROLES:
            return
        return self.users.update({"$set" : { "role" : role_name }}, {"_id" : user_id})

    def create_role(self, role_name : str, user_id : str):
        '''
            create role and add it to user
            replaces old role
        '''
        global ROLES
        if user_id is None or role_name is None:
            return
        role_name = role_name.upper()
        if not role_name in ROLES or not self.users.exist(user_id):
            return
        self.remove_role(user_id)
        self.roles.create({"role" : role_name, "user_id" : user_id, "creation_date" : str(datetime.utcnow())})
        self.set_user_role(role_name, user_id)

    def remove_role(self, user_id):
        if not self.users.exist(user_id): return
        self.roles.delete({"user_id" : user_id})
        self.users.update({"$set" : { "role" : "" }}, {"_id" : user_id})

    def delete_user(self, user_id):
        if not self.users.exist(user_id): return
        self.users.delete({"_id" : user_id})
        self.roles.delete({"user_id" : user_id})

    def get_noroles_user_choices(self) -> list:
        '''
        returns list with mails/logins
        of users with no role assigned
        '''
        res = self.users.get(filter={"role" : ""}, projection=["mail", "_id", "tg_login"])
        res = [(x["_id"], x["mail"] if x["mail"] != "" else x["tg_login"] ) for x in res]
        return res

    def create_user(self, user_data : dict):
        user_data["access_token"] = generate_user_token()
        user_data["role"] = ""
        user_data["mail"] = user_data.get("mail", "")
        user_data["tg_login"] = user_data.get("tg_login", "")
        user_data["auth_methods_submitted"] = user_data.get("auth_methods_submitted", [])
        return self.users.create(user_data)

    def user_token_can(self, token, action):
        '''
            check if user with given token has access to given action
        '''
        user = self.users.get({"access_token" : token})
        if len(user) == 0:
            return False
        user = user[0]
        roles = self.roles.get({"user_id" : user["_id"]})
        for role in roles:
            if action in PERMISSIONS[role["role"]]:
                return True
        self.check_user_roles_ttl()
        return False

    def user_id_can(self, user_id, action):
        '''
            check if user has access to given action
        '''
        roles = self.roles.get({"user_id" : user_id})
        for role in roles:
            if action in PERMISSIONS[role["role"]]:
                return True
        self.check_user_roles_ttl()
        return False

    def check_user_roles_ttl(self):
        """
            removes role field from user if role expired
        """
        users = self.users.get()
        for user in users:
            if user["role"] != "":
                uid = user["_id"]
                roles = self.roles.get({"user_id" : uid})
                if len(roles) == 0:
                    self.remove_role(uid)


if __name__ == "__main__":
    # dev tests
    dao = WikiAuthDAO()
    # dao.roles.delete({"user_id": "5eb81f6009205238f0972bda"})
    # dao.users.delete({})
    # dao.roles.delete({})
    # uid = dao.create_user({"mail" : "test@mail.ru"})["_id"]

    # print(dao.get_noroles_user_choices())
    # dao.set_user_role("USER", uid)
    # print(dao.user_id_can(uid, "view"))

    # dao.create_role("ADMIN", uid)
    # print(dao.users.get())
    # print(dao.roles.get())
    # print(dao.user_id_can(uid, "edit"))
    # sleep(180)
    # dao.check_user_roles_ttl()
    # print(dao.roles.get())
    # print(dao.users.get())

    # print(dao.get_noroles_user_choices())

    # print(dao.user_id_can(uid, "edit"))

    # dao.remove_role(uid)
    # dao.delete_user(uid)

    # print(dao.get_noroles_user_choices())
    # print(dao.users.get())
    # print(dao.roles.get())

