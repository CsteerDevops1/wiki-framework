from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import TG_TOKEN, PROXY_AUTH, PROXY_URL, get_from_wiki
import re
import logging


# Initialize bot and dispatcher
if PROXY_AUTH:
    bot = Bot(token=TG_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
else:
    bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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
    res = get_from_wiki(id=_id)["_id"]
    if res:
        async with state.proxy() as idp:
            idp["_id"] = res["_id"]
        await EditProcess._id.set()
        await message.answer(f"Found : {res['name']}")
        await message.answer("Are you sure want to edit this one?", reply_markup=get_replymarkup_yesno())


@dp.message_handler(state='*', regexp='^[n|N]ame\s*:?\s*(.*)')
async def find_by_name(message: types.Message, state: FSMContext):
    name = re.match("^[n|N]ame\s*:?\s*(.*)", message.text).group(1)
    res = get_from_wiki(name=name)["name"]
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
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Yes':
            await EditProcess.old_field.set()
            logging.info(f"Yes to {data['_id']}")
            # send choose field markup
        elif message.text == 'No':
            logging.info(f"NO to {data['_id']}")
            await state.finish()
            await message.answer('Ok', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler()
async def unexpected(message: types.Message):
    await message.answer("Didn't understand your message")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)