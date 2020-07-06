import os
from dotenv import load_dotenv
load_dotenv()
import base64

HOST = os.getenv('FLASK_HOST')
PORT = os.getenv('FLASK_PORT')
PATH = "/api/wiki"
ADDRESS = f"http://{HOST}:{PORT}{PATH}"

EXAMPLE_DOC = {
            "name" : "123",
            "russian_name" : "",
            "description" : "val_post1",
            "russian_description" : "",
            "tags" : ["fds", "123"],
            "text" : "text",
            # "creation_date" : str(datetime.utcnow()),
            "synonyms" : [],
            "relations" : [],
            # "attachments" : [{"content_type" : "image/png", "content_data" : b"bytes".decode()}]
            }

def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')


def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))