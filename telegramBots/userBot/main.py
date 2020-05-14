import os, re, json, hashlib, aiohttp
from  typing import List, Dict, Tuple, Union
from requests import get
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle 

from config import form_input_file, form_message_list, \
    reply_attachments, filter_attachments
from middlewares import LogMiddleware
from config import Lang
import buttons
from ApiConnection import ApiConnection
from ObjectMessage import ObjectMessage
from ObjectList import ObjectList

load_dotenv()
TOKEN    = os.getenv('USER_BOT_TOKEN')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
API_PATH = "/api/wiki"
API_ADDRESS = f"http://{API_HOST}:{API_PORT}{API_PATH}"
AUTOSUGGEST_ADDERSS = f"http://{API_HOST}:{API_PORT}{API_PATH}/autosuggest"

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
dp.middleware.setup(LogMiddleware())
conn = ApiConnection(API_HOST, API_PORT)



@dp.inline_handler()
async def inline_search(inline_query: InlineQuery):
    #TODO: don't forget to set cache_time=1 for testing (default is 300s or 5m)
    ct = 1 
    user_typing = inline_query.query or 'none'
    ret = get(AUTOSUGGEST_ADDERSS, params={'data': user_typing, 'complete' : 'True'})
    answer = json.loads(ret.text.encode("utf8"))['completed']
    if len(answer) == 0:
        result_id: str = hashlib.md5(user_typing.encode()).hexdigest()
        title = 'Nothing found'
        content = InputTextMessageContent(
            f"Not found: {user_typing}"
        )
        item = InlineQueryResultArticle(
            id=result_id,
            title=title,
            # description=description,
            input_message_content=content
        )
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=ct)
    else:
        results = []
        result_id: str = hashlib.md5(user_typing.encode()).hexdigest()
        for i, item in enumerate(answer):
            title = item['name']
            description = item['description']
            content = InputTextMessageContent(
                f"*{item['name']}*\n" \
                f"{item['description']}",
                parse_mode='Markdown'
            )
            results.append(InlineQueryResultArticle(
                id=result_id+item['_id'],
                title=title,
                description=description,
                input_message_content=content
            ))
        await bot.answer_inline_query(inline_query.id, results=results, cache_time=ct)


@dp.message_handler(commands=['start'])
async def welcome_msg(message: types.Message):
    #TODO: add full description
    text = "Hello there\n\n" \
           "This bot can search in wiki database " \
           "and return the result.\n"     
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
    text = "Text me a search query or use following commands:\n" \
           "/find \\[ _word_ ]\n" \
           "/find\\_id \\[ \\_id ] if you want to search by id\n" \
           "/list\\_all to get all records"
    await message.answer(text, parse_mode='Markdown')


@dp.message_handler(commands=['find'])
async def find(message: types.Message):
    try:
        name = re.match(r'/find\s([\w -]+).*', message.text, flags=re.IGNORECASE).group(1)
    except:
        return
    await ObjectList(conn, name).answer_to(message)


@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    try:
        name = re.match(r'/get_json\s([\w -]+).*', message.text, flags=re.IGNORECASE).group(1)
    except:
        return
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
    try:
        _id = re.match(r'/find_id\s([\w -]+).*', message.text, flags=re.IGNORECASE).group(1)
    except:
        return
    await ObjectMessage(conn, _id).answer_to(message)


@dp.message_handler(commands=['list_all'])
async def list_all(message: types.Message):
    await ObjectList(conn).answer_to(message)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_msg(message: types.Message):
    name = message.text.strip().split('\n')[0]
    #TODO: set correct limit of search querry length
    if len(name) > 50:
        return
    await ObjectList(conn, name).answer_to(message)


@dp.callback_query_handler(lambda c: re.match(r'sp:', c.data))
async def swap_page(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    _, data, page = callback_query.data.split(':')
    page = int(page)
    await ObjectList(conn, data, page=page).update_msg(callback_query.message)
    

@dp.callback_query_handler(lambda c: re.match(r'att:', c.data))
async def get_attachment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    _, _id, num = callback_query.data.split(':')
    num = int(num)
    await ObjectMessage(conn, _id).reply_attachment(num, callback_query.message)


@dp.callback_query_handler(lambda c: re.match(r'lang:', c.data))
async def update_msg_lang(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    prev_exp = callback_query.message.reply_markup.inline_keyboard[0][0].callback_data
    prev_exp = True if 'less:' in prev_exp else False
    new_lang, _id = callback_query.data.replace('lang:', '').split(':')
    new_lang = Lang.ENG if new_lang == 'en' else Lang.RUS
    await ObjectMessage(conn, _id, expanded=prev_exp, lang=new_lang).update_msg(callback_query.message)
    

@dp.callback_query_handler(lambda c: re.match(r'(more)|(less):', c.data))
async def update_msg_size(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    prev_lang = callback_query.message.reply_markup.inline_keyboard[0][1].callback_data
    prev_lang = Lang.ENG if 'lang:ru' in prev_lang else Lang.RUS
    _id = re.findall(r':(.*)', callback_query.data)
    if len(_id) == 1:
        _id = _id[0]
        if re.match(r'more:.*', callback_query.data):
            await ObjectMessage(conn, _id, expanded=True, lang=prev_lang).update_msg(callback_query.message)
        if re.match(r'less:.*', callback_query.data):
            await ObjectMessage(conn, _id, expanded=False, lang=prev_lang).update_msg(callback_query.message)
    else:
        await bot.send_message('Error occured')


@dp.callback_query_handler(lambda c: re.match(r'id:', c.data))
async def get_object(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    _id = re.findall(r'id:(.*)', callback_query.data)
    if len(_id) == 1:
        _id = _id[0]
        await ObjectMessage(conn, _id).answer_to(callback_query.message)
    else:
        await bot.send_message('Error occured')


def main():
    print('---- started ----')
    executor.start_polling(dp, skip_updates=True)    
    print('---- exited ----')


if __name__ == "__main__":
    main()
