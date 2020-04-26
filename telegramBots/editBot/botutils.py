import base64
from itertools import islice
from aiogram import types
import requests
import logging
from config import WIKI_API, WIKI_API_AUTOSUGGET, SUPPORTED_MEDIA_TYPES
import io
from collections.abc import Sequence, Iterable
import filetype
import pprint
import re


def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')

def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

def form_input_file(src: str):
    tmp = io.BytesIO()
    tmp.write(bytes_from_str(src))
    tmp.seek(0)
    return tmp

async def reply_attachments(message: types.Message, attachments: list):
    if attachments is None:
        return
    for item in attachments:
        try:
            if re.match(r'image\/.*', item['content_type'], flags=re.IGNORECASE):
                photo_d = form_input_file(item['content_data'])
                await message.answer_photo(photo_d)
            elif re.match(r'audio\/.*', item['content_type'], flags=re.IGNORECASE):
                video_d = form_input_file(item['content_data'])
                await message.answer_audio(video_d)
            elif re.match(r'video\/.*', item['content_type'], flags=re.IGNORECASE):
                video_d = form_input_file(item['content_data'])
                await message.answer_video(video_d)
            elif re.match(r'application\/.*', item['content_type'], flags=re.IGNORECASE):
                #TODO: need name of file
                file_d = form_input_file(item['content_data'])
                await message.answer_document(file_d)
        except Exception as e:
            logging.error(f'Error uploading file: {e}')

def format_page_info(word : dict) -> str:
    for key in word:
        if type(word[key]) == type("") and len(word[key]) > 50:
            word[key] = word[key][:50] + "..."
    return pprint.pformat(word, depth=2, compact=True).strip("{}")

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

def post_to_wiki(data: dict):
    '''returns None on fail'''
    res = requests.post(WIKI_API, json=data, 
                    headers={'Content-Type': 'application/json', "accept": "application/json"})
    if res.status_code != 201:
        return None
    else:
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


def set_default_values(data: dict):
    ''' 
    set values to defautls in dict
    keys : ["name", "russian_name", "description", "russian_description", "synonyms", "tags", "relations", "attachments"]
    '''
    data["name"] = ""
    data["russian_name"] = ""
    data["description"] = ""
    data["russian_description"] = ""
    data["synonyms"] = []
    data["tags"] = []
    data["relations"] = []
    data["attachments"] = []
    

# -------------------- MARKUPS ---------------------------------------------

def get_replymarkup_names(names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for name in names:
        markup.add(name["name"] + f" ({name['_id'][-5:]})")
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

def get_replymarkup_cancel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Cancel")
    return markup
