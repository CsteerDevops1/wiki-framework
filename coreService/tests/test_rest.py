import sys
sys.path.append(".")
from requests import get, put, delete, post
import json
from config import *


data = json.dumps(EXAMPLE_DOC)

res = post(ADDRESS, data=json.dumps(EXAMPLE_DOC), 
            headers={'Content-Type': 'application/json', "accept": "application/json"})
created_id = json.loads(res.text).get("_id", None)
print("Test post : ", res.status_code == 201, " _id : ", created_id)

res = get(ADDRESS, params={"_id" : created_id})
code = res.status_code
res = json.loads(res.text)
print("Test get : ", len(res) == 1, f" Code : {code}")

res = put(ADDRESS, params={"_id" : created_id}, data=json.dumps({"name" : "check_rest_name"}),
            headers={'Content-Type': 'application/json', "accept": "application/json"})
code = res.status_code
res = json.loads(res.text)
print("Test put : ", res == 1, f" Code : {code}")

res = delete(ADDRESS, params={"_id" : created_id})
code = res.status_code
res = json.loads(res.text)
print("Test delete : ", res == 1, f" Code : {code}")

