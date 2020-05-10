import json
from typing import List, Dict
from requests import get

class ApiConnection():
    def __init__(self, HOST: str, PORT: str):
        self.HOST = HOST
        self.PORT = PORT
    def get_object(self, _id: str) -> Dict:
        # ret = get(self.HOST, params={'_id': _id}, headers={'X-Fields': '_id, name, description, text'}).text
        ret = get(self.HOST, params={'_id': _id}).text
        ret = json.loads(ret)[0]
        return ret