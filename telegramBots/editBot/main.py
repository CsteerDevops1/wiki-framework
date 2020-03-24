from aiogram import Bot, Dispatcher, executor, types
from config import TG_TOKEN, PROXY_AUTH, PROXY_URL, get_from_wiki
import re


# Initialize bot and dispatcher
if PROXY_AUTH:
    bot = Bot(token=TG_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
else:
    bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "info"])
async def start(message: types.Message):
    await message.answer('Enter id or name of object you want to edit')


@dp.message_handler(regexp='^[i|I][d|D]\s*:?\s*([0-9a-z]{24})')
async def find_by_id(message: types.Message):
    _id = re.match("^[i|I][d|D]\s*:?\s*([0-9a-z]{24})", message.text).group(1)
    res = get_from_wiki(id=_id)["_id"]
    if res:
        await message.answer(f"Found : {res['name']}")


@dp.message_handler(regexp='^[n|N]ame\s*:?\s*(.*)')
async def find_by_name(message: types.Message):
    name = re.match("^[n|N]ame\s*:?\s*(.*)", message.text).group(1)
    res = get_from_wiki(name=name)["name"]
    for word in res:
        await message.answer(f"Found : {word['name']}")
    if len(res) == 0:
        await message.answer(f"Nothing found for {name}")


@dp.message_handler()
async def unexpected(message: types.Message):
    await message.answer("Didn't understand your message")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)