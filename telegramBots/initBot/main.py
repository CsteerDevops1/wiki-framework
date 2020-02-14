from telegram import Update
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from telegramBots.initBot.config import TG_TOKEN
from telegramBots.initBot.config import TG_API_URL

def do_start(bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello World!"
    )


def do_echo(bot, update: Update):  # processing message from client
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"I am just a bot I can't talk now\n "
             f"Your message: {text}"
    )

def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)  # taking only 'text'

    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()