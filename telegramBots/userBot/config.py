import base64
from typing import List, Dict, Tuple
from aiogram import types
from io import BytesIO
from aiogram.types.input_file import InputFile

def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')


def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))

def form_input_file(src: str) -> InputFile:
    tmp = BytesIO()
    tmp.write(bytes_from_str(src))
    tmp.seek(0)
    return InputFile(tmp)

def form_message_list(answer: List[Dict]) -> Tuple:
    kb = types.InlineKeyboardMarkup(row_width=5)
    tmp = [types.InlineKeyboardButton(str(i+1), callback_data=f"id:{item['_id']}") for i, item in enumerate(answer)]
    kb.add(*tmp)
    text = '\n'.join( [f"{i+1}. {item['name']} id:{item['_id'][-4:]}" for i, item in enumerate(answer)] )
    return (text, kb)

