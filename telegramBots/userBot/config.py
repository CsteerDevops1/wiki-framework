import re
import base64
from typing import List, Dict, Tuple, Union
from aiogram import types
from io import BytesIO
from aiogram.types.input_file import InputFile
from aiogram.utils.exceptions import BadRequest

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

async def reply_attachments(message: types.Message, attachments: List[Dict]):
    if attachments is None:
        return
    for item in attachments:
        try:
            if re.match(r'image\/.*', item['content_type'], flags=re.IGNORECASE):
                photo_d = form_input_file(item['content_data'])
                await message.answer_photo(photo_d)
            if re.match(r'audio\/.*', item['content_type'], flags=re.IGNORECASE):
                video_d = form_input_file(item['content_data'])
                await message.answer_audio(video_d)
            if re.match(r'video\/.*', item['content_type'], flags=re.IGNORECASE):
                video_d = form_input_file(item['content_data'])
                await message.answer_video(video_d)
            if re.match(r'application\/.*', item['content_type'], flags=re.IGNORECASE):
                #TODO: need name of file
                file_d = form_input_file(item['content_data'])
                await message.answer_document(file_d)
        except BadRequest as e:
            print('Error uploading file:', e, flush=True)

def filter_attachments(obj: Union[Dict, None]) -> Tuple:
    if 'attachments' in obj.keys():
        attachments = obj['attachments']
        obj.pop('attachments')
        return (obj, attachments)
    else:
        return (obj, None)
