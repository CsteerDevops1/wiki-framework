import json
import base64
import sys
from requests import post

ADDRESS = "http://188.124.37.185:5000/api/wiki"


def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')


def send(data):
    '''send a record to API'''
    return post(ADDRESS, data=json.dumps(data),
           headers={'Content-Type': 'application/json', "accept": "application/json"})


def push(data):
    '''send all data to API'''
    for record in data:
        for obj in record["attachments"]:
            with open(obj["content_data"], "rb") as f:
                content = bytes_to_str(f.read())
            obj["content_data"] = content
        resp = send(record)

        if not resp.ok:
            print("{} {}".format(record["name"], resp.text))

for f in sys.argv[1:]:
    data = json.load(open(f)) 
    push(data)
    print("File {} succesful uploaded".format(f))



