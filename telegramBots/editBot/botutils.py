import base64
from itertools import islice
from aiogram import types
import requests
import logging
from config import WIKI_API, WIKI_API_AUTOSUGGET, SUPPORTED_MEDIA_TYPES
import io
from collections.abc import Sequence, Iterable
import filetype


def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

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

async def download_media_from_msg(message: types.Message) -> dict:
    '''
       Returns downloaded content in format :
       {
           "content_type" : mime_type,
           "content_data" : bytes_to_str(data.read())
       } 
       OR None on error.
    '''
    global SUPPORTED_MEDIA_TYPES
    
    content_type = message.content_type
    if content_type not in SUPPORTED_MEDIA_TYPES:
        logging.warning(f"download_media_from_msg function was called with unsupported content_type '{content_type}'")
        return
    try:
        content = message.__getattribute__(content_type)
    except AttributeError as err:
        logging.error(f"Can't get {content_type} from message. Canceling download_media_from_msg function")
        return

    try:
        content = content[0] # best way to handle content that sometiems is some kind of array
    except Exception:
        pass
    if content is None:
        logging.warning(f"{content_type} field in message is None. Canceling download_media_from_msg function")
        return

    data = io.BytesIO()
    await content.download(data)
    mime_type = filetype.guess(data).mime
    data.seek(0)
    item = {
        "content_type" : mime_type,
        "content_data" : bytes_to_str(data.read())
    }
    return item

# -------------------- MARKUPS ---------------------------------------------

def get_replymarkup_names(names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for name in names:
        markup.add(name["name"])
    markup.add("Cancel")
    return markup

def get_replymarkup_yesno():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Yes", "No")
    markup.add("Cancel")
    return markup

def get_replymarkup_fields(word):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for fields in split_every(2, word):
        markup.add(*fields)
    markup.add("Cancel")
    return markup

def get_replymarkup_finish():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Finish")
    markup.add("Cancel")
    return markup
