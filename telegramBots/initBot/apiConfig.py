import os
from dotenv import load_dotenv
load_dotenv()
import base64
import requests
HOST = os.getenv('FLASK_HOST')
PORT = os.getenv('FLASK_PORT')
PATH = "/api/wiki"
ADDRESS = os.getenv("ADDRESS")
# ADDRESS = f"http://{HOST}:{PORT}/api/wiki"
def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')


def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))

EXAMPLE_DOC = {
            "name": "",
            "description": "",
            "tags": [],
            "text": "",
            # "creation_date" : str(datetime.utcnow()),
            "synonyms": [],
            "relations": [],
            "attachments": []
            }

