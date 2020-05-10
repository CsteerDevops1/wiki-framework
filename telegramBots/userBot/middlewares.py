import time
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class LogMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        t = time.strftime('%Y-%m-%d_%H:%M', time.localtime())
        user = message.from_user.username
        try: text = message.text
        except: text = None
        print(f"[{t}]: message from @{user} | text: '{text}'")