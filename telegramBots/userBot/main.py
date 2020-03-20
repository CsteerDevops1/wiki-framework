import os, re, json
from  typing import List, Dict, Tuple, Union
import hashlib
from requests import get
from dotenv import load_dotenv
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle 
from aiogram.utils.exceptions import BadRequest
from config import form_input_file
from typos import get_possible_typos

load_dotenv()
TOKEN    = os.getenv('USER_BOT_TOKEN')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
API_PATH = "/api/wiki"
API_ADDRESS = f"http://{API_HOST}:{API_PORT}{API_PATH}"

# optional 
PROXY_URL       = os.getenv('PROXY_URL')
PROXY_LOGIN     = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD  = os.getenv('PROXY_PASSWORD')
if PROXY_URL != None:
    PROXY_AUTH = aiohttp.BasicAuth(
        login=PROXY_LOGIN,
        password=PROXY_PASSWORD
    )
    bot = Bot(token=TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
else:
    bot = Bot(token=TOKEN)

dp = Dispatcher(bot)

def filter_attachments(obj: Union[Dict, None]) -> Tuple:
    if 'attachments' in obj.keys():
        attachments = obj['attachments']
        obj.pop('attachments')
        return (obj, attachments)
    else:
        return (obj, None)


@dp.inline_handler()
async def inline_search(inline_query: InlineQuery):
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example I'll generate it based on text because I know, that
    # only text will be passed in this example
    user_typing = inline_query.query or 'none'
    ret = get(API_ADDRESS, params={'name': user_typing})
    answer = json.loads(ret.text.encode("utf8"))
    text = f'Search query:  *{user_typing}* \n'
    if len(answer) == 0:
        text = text + 'Nothing found'
        title = 'Nothing found'
    else:
        title = user_typing.capitalize()
        answer, attachments = filter_attachments(answer[0])
        prettified = json.dumps(answer, indent=2, ensure_ascii=False).encode('utf8').decode()
        text = text + f"```\n{prettified}\n```"
    input_content = InputTextMessageContent(text, parse_mode='Markdown')
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=title,
        input_message_content=input_content,
        description=text
    )
    #TODO: don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


@dp.message_handler(commands=['start'])
async def welcome_msg(message: types.Message):
    #TODO: add full description
    text = "Hello there\n\n" \
           "This bot can search in wiki database " \
           "and return the result.\n" \
           "Usage: /find \\[ _search querry_ ]\n"
    await message.answer(text, parse_mode='Markdown')


@dp.message_handler(commands=['help'])
async def help_msg(message: types.Message):
    """
        List of commands:
            help - Description
            find - Search something
            find_id - Search by id
            list_all - Get list of all records
            get_json - Debug
    """
    text = "Usage: /find \\[ _word_ ]\n" \
           "/find\\_id \\[ \\_id ] if you want to search by id\n" \
           "/list\\_all to get all records"
    await message.answer(text, parse_mode='Markdown')


@dp.message_handler(commands=['find'])
async def find(message: types.Message):
    name = re.match(r'/find\s(\w+).*', message.text, flags=re.IGNORECASE).group(1)
    ret = get(API_ADDRESS, params={'name': rf'^{get_possible_typos(name)}\b', 'regex' : 'True'})
    answer = json.loads(ret.text.encode("utf8"))
    
    if len(answer) == 0:
        await message.answer('Nothing was found')
    else:
        for word in answer:
            word_info, attachments = filter_attachments(word)
            msg =  f"*{word_info['name'].capitalize()}*:\n"
            msg += f"{word_info['description']}"
            await message.answer(f"{msg}", parse_mode='Markdown')
            if attachments != None:
                await reply_attachments(message, attachments)


@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    name = re.match(r'/get_json\s(\w+).*', message.text, flags=re.IGNORECASE).group(1)
    ret = get(API_ADDRESS, params={'name': name})
    answer = json.loads(ret.text.encode("utf8"))
    if len(answer) == 0:
        await message.answer('Nothing was found')
    else:
        answer, attachments = filter_attachments(answer[0])
        prettified = json.dumps(answer, indent=2, ensure_ascii=False).encode('utf8').decode()
        await message.answer(f"```\n{prettified}\n```", parse_mode='Markdown')
        if attachments != None:
            await reply_attachments(message, attachments)


@dp.message_handler(commands=['find_id'])
async def find_id(message: types.Message):
    name = re.match(r'/find_id\s(\w+).*', message.text, flags=re.IGNORECASE).group(1)
    ret = get(API_ADDRESS, params={'_id': name})
    answer = json.loads(ret.text.encode("utf8"))
    
    if len(answer) == 0:
        await message.answer('Nothing was found')
    else:
        answer, attachments = filter_attachments(answer[0])
        prettified = json.dumps(answer, indent=2, ensure_ascii=False).encode('utf8').decode()
        msg = f"*{answer['name'].capitalize()}*:\n"
        msg += f"{answer['description']}"
        await message.answer(f"{msg}", parse_mode='Markdown')
        if attachments != None:
            await reply_attachments(message, attachments)


@dp.message_handler(commands=['list_all'])
async def list_all(message: types.Message):
    ret = get(API_ADDRESS, headers={'X-Fields': '_id, name'})
    answer: List[Dict] = json.loads(ret.text)
    msg = '\n'.join([f"*{x['name']}*: `{x['_id']}`" for x in answer])
    await message.answer(msg, parse_mode='Markdown')


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


@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_msg(message: types.Message):
    name = message.text.strip().split('\n')[0]
    #TODO: set correct limit of search querry length
    if len(name) > 50:
        return
    ret = get(API_ADDRESS, params={'name': rf'^{get_possible_typos(name)}', 'regex' : 'True'})
    answer: List[Dict] = json.loads(ret.text)
    if len(answer) == 0:
        await message.answer('Sorry, nothing found')
    else:
        kb = types.InlineKeyboardMarkup(row_width=5)
        tmp = [types.InlineKeyboardButton(str(i+1), callback_data=f"id:{item['_id']}") for i, item in enumerate(answer)]
        kb.add(*tmp)
        text = '\n'.join( [f"{i+1}. {item['name']}" for i, item in enumerate(answer)] )
        await message.answer(text, reply_markup=kb)


def main():
    executor.start_polling(dp, skip_updates=True)    


if __name__ == "__main__":
    main()
