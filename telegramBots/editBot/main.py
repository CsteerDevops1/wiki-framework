from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import TG_TOKEN, PROXY_AUTH, PROXY_URL, SUPPORTED_MEDIA_TYPES, REQUIRED_WIKI_FIELDS
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
    edit_or_delete = State() # user choose whether to edit or delete obj
    delete_confirmation = State() # user approved deleting
    old_field = State() # user selected field for editing
    new_field_text = State() # user entered new text data for field
    new_field_media = State() # user is entering new media data for field


class CreateProcess(StatesGroup):
    fields_choosing = State() # user is entering fields for new object
    fields_set_value = State() # waiting for the user to submit a new value
    confiramtion = State() # waiting for user to accept


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


@dp.message_handler(commands=["create"])
async def create_new_obj(message: types.Message, state: FSMContext):
    await CreateProcess.fields_choosing.set()
    async with state.proxy() as data:
        data["new_obj_data"] = {}
        botutils.set_default_values(data["new_obj_data"])
        await message.answer('Current new object is :')
        await message.answer(botutils.format_page_info(data["new_obj_data"]))
    await message.answer('Select a field and send value for this field. Type "Done" to finish.', reply_markup=botutils.get_replymarkup_fields(REQUIRED_WIKI_FIELDS))


@dp.message_handler(lambda msg : msg.text.lower() != "done", state=CreateProcess.fields_choosing)
async def process_new_fields(message: types.Message, state: FSMContext):
    global ARRAY_FIELDS, MEDIA_CONTENT_FIELDS
    field = message.text
    async with state.proxy() as data:
        data["creating_field"] = field
    await message.answer(f"Send value for field '{field}'", reply_markup=botutils.get_replymarkup_cancel())
    if field in ARRAY_FIELDS:
        await message.answer(f"This field is supposed to be an array, send text values separated with ','")
    elif field in MEDIA_CONTENT_FIELDS:
        await message.answer(f"This field is supposed to keep media content")
    await CreateProcess.fields_set_value.set()


@dp.message_handler(state=CreateProcess.fields_set_value, content_types=SUPPORTED_MEDIA_TYPES + ["text"])
async def process_new_fields(message: types.Message, state: FSMContext):
    global ARRAY_FIELDS, MEDIA_CONTENT_FIELDS
    async with state.proxy() as data:
        field = data["creating_field"]
        if field in ARRAY_FIELDS:
            data["new_obj_data"][field] = [x.strip() for x in message.text.strip().lstrip("[").rstrip("]").split(",")]
        elif field in MEDIA_CONTENT_FIELDS:
            content = await botutils.download_media_from_msg(message)
            if content is None:
                await message.answer("Wrong value")
                return
            data["new_obj_data"][field].append(content)
        else:
            data["new_obj_data"][field] = message.text
        await message.answer('Current new object is :')
        await message.answer(botutils.format_page_info(data["new_obj_data"]))
        await CreateProcess.fields_choosing.set()
        await message.answer('Select a field and send value for this field. Type "Done" to finish.', reply_markup=botutils.get_replymarkup_fields(REQUIRED_WIKI_FIELDS))
        

@dp.message_handler(Text(equals='Done', ignore_case=True), state=CreateProcess.fields_choosing)
async def confirm_new_obj(message: types.Message, state: FSMContext):
    await CreateProcess.confiramtion.set()
    await message.answer("Are you sure you want to create this one?", reply_markup=botutils.get_replymarkup_yesno())


@dp.message_handler(state=CreateProcess.confiramtion)
async def save_new_obj(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Yes':
            logging.debug(f"User {message.from_user.id} creating new obj")
            new_obj = data["new_obj_data"]
            if botutils.post_to_wiki(new_obj) is not None:
                await message.answer('A new object has been added to the database', reply_markup=types.ReplyKeyboardRemove())
            else:
                await message.answer('An error occurred while adding to the database', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        elif message.text == 'No':
            await state.finish()
            await message.answer('Ok', reply_markup=types.ReplyKeyboardRemove())


# TODO: edit to hanndle inline bot, not the html_text
@dp.message_handler(lambda message: re.match('^<b>(.+)</b>', message.html_text), state='*')
async def find_from_search_bot(message: types.Message, state: FSMContext):
    name = re.match('^<b>(.+)</b>', message.html_text).group(1)
    res = botutils.get_from_wiki(name=name, ret_fields=["name"])["name"]
    await EditProcess.name.set()
    async with state.proxy() as data:
        data['names'] = {word['_id'] : word['name'] for word in res}
    await message.answer("Which word do you want to change?", reply_markup=botutils.get_replymarkup_names(res))


@dp.message_handler(state='*', regexp='^/?[i|I][d|D]\s*:?\s*([0-9a-z]{24})')
async def find_by_id(message: types.Message, state: FSMContext):
    _id = re.match("^/?[i|I][d|D]\s*:?\s*([0-9a-z]{24})", message.text).group(1)
    res = botutils.get_from_wiki(id=_id, ret_fields=["name"])["_id"]
    if res:
        async with state.proxy() as idp:
            idp["_id"] = res["_id"]
        await EditProcess._id.set()
        await message.answer(f"Found : {res['name']}")
        await message.answer("Are you sure you want to edit this one?", reply_markup=botutils.get_replymarkup_yesno())


@dp.message_handler(state='*', regexp='^/?[n|N]ame\s*:?\s*(.+)')
async def find_by_name(message: types.Message, state: FSMContext):
    name = re.match("^/?[n|N]ame\s*:?\s*(.+)", message.text).group(1)
    res = botutils.get_from_wiki(name=name, ret_fields=["name"])["name"]
    if len(res) == 0:
        await message.answer(f"Nothing found for {name}")
        return
    await EditProcess.name.set()
    async with state.proxy() as data:
        data['names'] = {word['_id'] : word['name'] for word in res}
    await message.answer("Which word do you want to change? There are last 5 symbols of id in brackets.", reply_markup=botutils.get_replymarkup_names(res))


@dp.message_handler(state=EditProcess.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        matches = re.match("(.*) \((.+)\)", message.text)
        if matches is None:
            return
        name, _id = matches.groups()
        for word_id, word_name in data['names'].items():
            if word_name == name and str(word_id)[-5:] == _id:
                data["_id"] = word_id
                data["word_info"] = botutils.get_from_wiki(id=word_id)["_id"]
                word_info = data["word_info"]
                break
    await EditProcess._id.set()
    await message.answer(botutils.format_page_info(word_info))
    await message.answer("Are you sure you want to edit this one?", reply_markup=botutils.get_replymarkup_yesno())


@dp.message_handler(state=EditProcess._id)
async def process_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Yes':
            await EditProcess.edit_or_delete.set()
            await message.answer('Do you want to edit or delete object?', reply_markup=botutils.get_replymarkup_edit_delete())
        elif message.text == 'No':
            await state.finish()
            await message.answer('Ok', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=EditProcess.edit_or_delete)
async def edit_or_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["word_info"] = botutils.get_from_wiki(id=data["_id"])["_id"]
        word_info = data["word_info"]
        if message.text == 'Edit':
            logging.debug(f"User {message.from_user.id} is edititng {data['_id']}")
            del word_info["_id"]
            await EditProcess.old_field.set()
            await message.answer("What field do you want to change? (or create a new one)", reply_markup=botutils.get_replymarkup_fields(word_info))
        elif message.text == 'Delete':
            await EditProcess.delete_confirmation.set()
            await message.answer('Are you sure you want to delete this object?', reply_markup=botutils.get_replymarkup_yesno())


@dp.message_handler(state=EditProcess.delete_confirmation)
async def delete_obj(message: types.Message, state: FSMContext):
    if message.text == 'Yes':
        async with state.proxy() as data:
            _id = data["word_info"]["_id"]
        res = botutils.delete_wiki_obj(_id)
        await message.answer(f'{res} objects were deleted.', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif message.text == 'No':
        await state.finish()
        await message.answer('Ok', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=EditProcess.old_field)
async def process_field(message: types.Message, state: FSMContext):
    global MEDIA_CONTENT_FIELDS
    async with state.proxy() as data:
        data["old_field"] = message.text
        old_value = data["word_info"].get(message.text, "None")
        if old_value == "" or old_value == "None":
            old_value = "Field is empty"
    repl = botutils.get_replymarkup_cancel()
    await message.answer(f"Old value of '{message.text}' : ")
    if message.text in MEDIA_CONTENT_FIELDS:
        await botutils.reply_attachments(message, old_value)
        await EditProcess.new_field_media.set()
        async with state.proxy() as data:
            data["new_field_media"] = []
        repl = botutils.get_replymarkup_finish()
    else:
        await message.answer(old_value)
        await EditProcess.new_field_text.set()
    await message.answer(f"Send new value for this field.", reply_markup=repl)


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
    await message.answer(f"Send to API {len(new_attachments)} items.", reply_markup=botutils.get_replymarkup_yesno())
    if res == 1:
        await message.answer(f"You have succesfully updated field '{old_field}'.")
    else:
        await message.answer(f"Something went wrong, the field was not updated.")
    await message.answer(f"Do you want to change another one?")
    await EditProcess._id.set()


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
    if res == 1:
        await message.answer(f"You have succesfully updated the field '{old_field}'.", reply_markup=botutils.get_replymarkup_yesno())
    else:
        await message.answer(f"Something went wrong, the field is not updated.", reply_markup=botutils.get_replymarkup_yesno())
    await message.answer(f"Do you want to change another one?")
    await EditProcess._id.set()


@dp.message_handler()
async def unexpected(message: types.Message):
    await message.answer("Didn't understand your message")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
