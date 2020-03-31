from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import TG_TOKEN, PROXY_AUTH, PROXY_URL, SUPPORTED_MEDIA_TYPES
import botutils
import re
import logging


# Initialize bot and dispatcher
if PROXY_AUTH:
    bot = Bot(token=TG_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
else:
    bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ARRAY_FIELDS = ["synonyms", "tags", "relations"]
MEDIA_CONTENT_FIELDS = ["attachments"]


# States
class EditProcess(StatesGroup):
    _id = State() # user have chosen the id
    name = State() # user entered name, must ensure to set correct id
    old_field = State() # user have chosen field to edit
    new_field_text = State() # user entered new text data for field
    new_field_media = State() # user is entering new media data for field


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.debug(f'Cancelling state {current_state}')
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=["start", "info"])
async def start(message: types.Message):
    await message.answer('Enter id or name of object you want to edit. Format : "[name | id] object"')


# TODO: edit to hanndle inline bot, not the html_text
@dp.message_handler(lambda message: re.match('^<b>(.+)</b>', message.html_text), state='*')
async def find_from_search_bot(message: types.Message, state: FSMContext):
    name = re.match('^<b>(.+)</b>', message.html_text).group(1)
    res = botutils.get_from_wiki(name=name, ret_fields=["name"])["name"]
    await EditProcess.name.set()
    async with state.proxy() as data:
        data['names'] = {word['name'] : word['_id'] for word in res}
    await message.answer("Which word you want to change?", reply_markup=botutils.get_replymarkup_names(res))


@dp.message_handler(state='*', regexp='^[i|I][d|D]\s*:?\s*([0-9a-z]{24})')
async def find_by_id(message: types.Message, state: FSMContext):
    _id = re.match("^[i|I][d|D]\s*:?\s*([0-9a-z]{24})", message.text).group(1)
    res = botutils.get_from_wiki(id=_id, ret_fields=["name"])["_id"]
    if res:
        async with state.proxy() as idp:
            idp["_id"] = res["_id"]
        await EditProcess._id.set()
        await message.answer(f"Found : {res['name']}")
        await message.answer("Are you sure want to edit this one?", reply_markup=botutils.get_replymarkup_yesno())


@dp.message_handler(state='*', regexp='^[n|N]ame\s*:?\s*(.+)')
async def find_by_name(message: types.Message, state: FSMContext):
    name = re.match("^[n|N]ame\s*:?\s*(.+)", message.text).group(1)
    res = botutils.get_from_wiki(name=name, ret_fields=["name"])["name"]
    if len(res) == 0:
        await message.answer(f"Nothing found for {name}")
        return
    await EditProcess.name.set()
    async with state.proxy() as data:
        data['names'] = {word['name'] : word['_id'] for word in res}
    await message.answer("Which word you want to change?", reply_markup=botutils.get_replymarkup_names(res))


# TODO: keep ids in data['names'], to fix error with same names
@dp.message_handler(state=EditProcess.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["_id"] = data['names'][message.text]
    await EditProcess._id.set()
    await message.answer("Are you sure want to edit this one?", reply_markup=botutils.get_replymarkup_yesno())


@dp.message_handler(state=EditProcess._id)
async def process_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Yes':
            await EditProcess.old_field.set()
            logging.debug(f"User {message.from_user.id} is edititng {data['_id']}")
            word_info = botutils.get_from_wiki(id=data['_id'])["_id"]
            del word_info["_id"]
            await message.answer("What field you wish to change?", reply_markup=botutils.get_replymarkup_fields(word_info))
        elif message.text == 'No':
            await state.finish()
            await message.answer('Ok', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=EditProcess.old_field)
async def process_field(message: types.Message, state: FSMContext):
    global MEDIA_CONTENT_FIELDS
    async with state.proxy() as data:
        data["old_field"] = message.text
    repl = types.ReplyKeyboardRemove()
    if message.text in MEDIA_CONTENT_FIELDS:
        await EditProcess.new_field_media.set()
        async with state.proxy() as data:
            data["new_field_media"] = []
        repl = botutils.get_replymarkup_finish()
    else:
        await EditProcess.new_field_text.set()
    await message.answer(f"You have chosen to edit field '{message.text}'. Send new value for this.", reply_markup=repl)


@dp.message_handler(state=EditProcess.new_field_media, content_types=SUPPORTED_MEDIA_TYPES)
async def get_new_field_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _id = data["_id"]
    item = await botutils.download_media_from_msg(message)
    if item is not None:
        async with state.proxy() as data:
            data["new_field_media"].append(item)
        await message.answer(f"{item['content_type']} added to list. Type 'Finish' to update field.")
    else:
        await message.answer(f"Couldn't add {item['content_type']} to list.")


@dp.message_handler(Text(equals='finish', ignore_case=True), state=EditProcess.new_field_media)
async def finish_adding_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _id = data["_id"]
        new_attachments = data.get("new_field_media", [])
        old_field = data["old_field"]
    res = botutils.update_in_wiki(_id, {old_field : new_attachments})
    await state.finish()
    await message.answer(f"Send to API {len(new_attachments)} items.", reply_markup=types.ReplyKeyboardRemove())
    if res == 1:
        await message.answer(f"You have succesfully updated field '{old_field}'.")
    else:
        await message.answer(f"Something went wrong, field is not updated.")


@dp.message_handler(state=EditProcess.new_field_text, content_types=["text"])
async def get_new_field_value(message: types.Message, state: FSMContext):
    global ARRAY_FIELDS
    async with state.proxy() as data:
        _id = data["_id"]
        old_field = data["old_field"]
    if old_field in ARRAY_FIELDS:
        new_val = [x.strip() for x in message.text.strip().lstrip("[").rstrip("]").split(",")]
    else:
        new_val = message.text
    res = botutils.update_in_wiki(_id, {old_field : new_val})
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
