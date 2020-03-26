import logging
from dotenv import load_dotenv
import os
import aiohttp
import requests


# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
TG_TOKEN = os.getenv('USER_BOT_TOKEN')
PROXY_URL = os.getenv('PROXY_URL')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
WIKI_API = f"http://{API_HOST}:{API_PORT}/api/wiki"
WIKI_API_AUTOSUGGET = f"http://{API_HOST}:{API_PORT}/api/wiki/autosuggest"
if PROXY_URL != None:
    PROXY_AUTH = aiohttp.BasicAuth(login=PROXY_LOGIN, password=PROXY_PASSWORD)
    logging.info(f"Proxy is set to {PROXY_AUTH}")
else:
    PROXY_AUTH = None


def get_from_wiki(id=None, name=None, ret_fields : list = None):
    '''if ret_fields is None returns all the fields'''
    if ret_fields:
        headers = {'X-Fields' : ",".join(ret_fields)}
    else:
        headers = None
    if id:
        _id = requests.get(WIKI_API, params={"_id" : id},
                                headers=headers)
        logging.info(f"Searching in WIKI db for id {id}")
    if name:
        _name = requests.get(WIKI_API_AUTOSUGGET, 
                                params={"data" : name, 'correct' : "True"},
                                headers=headers)
        logging.info(f"Searching in WIKI db for name {name}")
    return {
        "_id" : _id.json()[0] if id is not None and len(_id.json()) == 1 else None,
        "name" : _name.json()["corrected"] if name is not None else None
    }


def update_in_wiki(id, data):
    res = requests.put(WIKI_API, params={"_id" : id}, json=data)
    return res.json()
