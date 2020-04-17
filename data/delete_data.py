import json
import sys
from requests import delete

ADDRESS = "http://188.124.37.185:5000/api/wiki"


def delete_record(name):
    '''delete request to API'''
    return delete(ADDRESS, params={"name" : name})


def delete_all(data):
    '''delete request for all data to API'''
    for record in data:
        resp = delete_record(record["name"])
        if not resp.ok:
            print("{} {}".format(record["name"], resp.text))

for f in sys.argv[1:]:
    data = json.load(open(f, "r")) 
    delete_all(data)
    print("File {} succesful deleted from DB".format(f))



