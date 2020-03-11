import os, re, json
from  typing import List, Dict, Tuple, Union
import hashlib
from requests import get
from dotenv import load_dotenv
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle 
from config import form_input_file

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
    text = "Usage: /find \\[ _word_ ]"
    await message.answer(text, parse_mode='Markdown')


@dp.message_handler(commands=['find'])
async def find(message: types.Message):
    name = re.match(r'/find\s(\w+).*', message.text, flags=re.IGNORECASE).group(1)
    ret = get(API_ADDRESS, params={'name': name})
    answer = json.loads(ret.text.encode("utf8"))
    
    if len(answer) == 0:
        await message.answer('Nothing was found')
    else:
        #TODO: rework to handle all answers in list
        answer, attachments = filter_attachments(answer[0])
        prettified = json.dumps(answer, indent=2, ensure_ascii=False).encode('utf8').decode()
        await message.answer(f"```\n{prettified}\n```", parse_mode='Markdown')
        if attachments != None:
            await reply_attachments(message, attachments)


async def reply_attachments(message: types.Message, attachments: List[Dict]):
    for item in attachments:
        # if item['content_type'] == 'image/jpg':
        if re.match(r'image\/.*', item['content_type'], flags=re.IGNORECASE):
            photo = form_input_file(item['content_data'])
            await message.answer_photo(photo)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_msg(message: types.Message):
    await message.answer('I\'m not talking yet')
    # if re.match(r'^debug', message.text, flags=re.IGNORECASE):
    #     name = re.match(r'debug\s(\w+).*[\n]?', message.text, flags=re.IGNORECASE).group(1)
    #     ret = get(API_ADDRESS, params={'name': name})
    #     answer = json.loads(ret.text)
    #     if len(answer) == 0:
    #         await message.answer('Nothing was found')
    #     else:
    #         prettified = json.dumps(json.loads(ret.text), indent=1).encode('utf8').decode()
    #         await message.answer(f"```\n{prettified}\n```", parse_mode='Markdown')

def main():
    executor.start_polling(dp, skip_updates=False)    


if __name__ == "__main__":
    main()
