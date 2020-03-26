from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import TG_TOKEN, PROXY_AUTH, PROXY_URL, get_from_wiki, update_in_wiki
from utils import *
import re
import logging
from itertools import islice
import io
import json


# Initialize bot and dispatcher
if PROXY_AUTH:
    bot = Bot(token=TG_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
else:
    bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ARRAY_FIELDS = ["synonyms", "tags", "relations"]


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

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

# States
class EditProcess(StatesGroup):
    _id = State() # user have chosen the id
    name = State() # user entered name, must ensure to set correct id
    old_field = State() # user have chosen field to edit
    new_field = State() # user entered new data for field


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=["start", "info"])
async def start(message: types.Message):
    await message.answer('Enter id or name of object you want to edit')


@dp.message_handler(state='*', regexp='^[i|I][d|D]\s*:?\s*([0-9a-z]{24})')
async def find_by_id(message: types.Message, state: FSMContext):
    _id = re.match("^[i|I][d|D]\s*:?\s*([0-9a-z]{24})", message.text).group(1)
    res = get_from_wiki(id=_id, ret_fields=["name"])["_id"]
    if res:
        async with state.proxy() as idp:
            idp["_id"] = res["_id"]
        await EditProcess._id.set()
        await message.answer(f"Found : {res['name']}")
        await message.answer("Are you sure want to edit this one?", reply_markup=get_replymarkup_yesno())


@dp.message_handler(state='*', regexp='^[n|N]ame\s*:?\s*(.+)')
async def find_by_name(message: types.Message, state: FSMContext):
    name = re.match("^[n|N]ame\s*:?\s*(.+)", message.text).group(1)
    res = get_from_wiki(name=name, ret_fields=["name"])["name"]
    if len(res) == 0:
        await message.answer(f"Nothing found for {name}")
        return
    await EditProcess.name.set()
    async with state.proxy() as data:
        data['names'] = {word['name'] : word['_id'] for word in res}
    await message.answer("Which word you want to change?", reply_markup=get_replymarkup_names(res))


@dp.message_handler(state=EditProcess.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["_id"] = data['names'][message.text]
    await EditProcess._id.set()
    await message.answer("Are you sure want to edit this one?", reply_markup=get_replymarkup_yesno())


@dp.message_handler(state=EditProcess._id)
async def process_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Yes':
            await EditProcess.old_field.set()
            logging.info(f"Yes to {data['_id']}")
            word_info = get_from_wiki(id=data['_id'])["_id"]
            del word_info["_id"]
            await message.answer("What field you wish to change?", reply_markup=get_replymarkup_fields(word_info))
        elif message.text == 'No':
            logging.info(f"NO to {data['_id']}")
            await state.finish()
            await message.answer('Ok', reply_markup=types.ReplyKeyboardRemove())



@dp.message_handler(state=EditProcess.old_field)
async def process_field(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["old_field"] = message.text
    await EditProcess.new_field.set()
    await message.answer(f"You have chosen to edit field '{message.text}'. Send new value for this.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=EditProcess.new_field, content_types=["audio"])
async def get_new_field_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _id = data["_id"]
        old_field = data["old_field"]
    if old_field != "attachments":
        await message.answer(f"You can't add media to this field. Canceled.")
        await state.finish()
        return
    audio_info = json.loads(message.audio.as_json())
    audio_data = io.BytesIO()
    await message.audio.download(audio_data)
    audio_item = {
        "content_type" : audio_info["mime_type"],
        "content_data" : bytes_to_str(audio_data.read()),
        "descritpion" : audio_info["title"]
    }
    res = update_in_wiki(_id, {old_field : [audio_item]})
    await state.finish()
    if res == 1:
        await message.answer(f"You have succesfully updated field '{old_field}'.")
    else:
        await message.answer(f"Something went wrong, field is not updated.")


@dp.message_handler(state=EditProcess.new_field, content_types=["photo"])
async def get_new_field_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _id = data["_id"]
        old_field = data["old_field"]
    if old_field != "attachments":
        await message.answer(f"You can't add media to this field. Canceled.")
        await state.finish()
        return
    new_val = []
    for photo in message.photo:
        photo_info = json.loads(photo.as_json())
        photo_data = io.BytesIO()
        await photo.download(photo_data)
        photo_item = {
            "content_type" : "image/jpeg",#photo_info["mime_type"],
            "content_data" : bytes_to_str(photo_data.read()),
            # "descritpion" : photo_info["title"]
        }
        new_val.append(photo_item)
    res = update_in_wiki(_id, {old_field : new_val})
    await state.finish()
    if res == 1:
        await message.answer(f"You have succesfully updated field '{old_field}'.")
    else:
        await message.answer(f"Something went wrong, field is not updated.")


@dp.message_handler(state=EditProcess.new_field, content_types=["text"])
async def get_new_field_value(message: types.Message, state: FSMContext):
    global ARRAY_FIELDS
    async with state.proxy() as data:
        _id = data["_id"]
        old_field = data["old_field"]
    if old_field in ARRAY_FIELDS:
        new_val = [x.strip() for x in message.text.strip().lstrip("[").rstrip("]").split(",")]
    else:
        new_val = message.text
    res = update_in_wiki(_id, {old_field : new_val})
    await state.finish()
    if res == 1:
        await message.answer(f"You have succesfully updated field '{old_field}'.")
    else:
        await message.answer(f"Something went wrong, field is not updated.")


@dp.message_handler()
async def unexpected(message: types.Message):
    await message.answer("Didn't understand your message")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
