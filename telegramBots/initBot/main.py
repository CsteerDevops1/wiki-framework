import logging
import json
from telegram import Update
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegramBots.media.fileManager import show_photo_info, save_pthoto
from telegramBots.initBot.config import TG_TOKEN
from telegramBots.initBot.config import TG_API_URL

photo_info = ""


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    global photo_info
    photo_info = str(update.message)
    # print(photo_info)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your message is:\n"
             f"{update.message.text}"
    )


def button_save_photo(update, context):
    global photo_info
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))
    if query.data == "Save":
        save_pthoto(photo_info)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Photo saved"
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Photo isn't saved"
        )


def get_photo(update, context):
    global photo_info
    photo_info = str(update.message)
    keyboard = [[InlineKeyboardButton("Save", callback_data='Save'),
                 InlineKeyboardButton("Cancel", callback_data='Cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'{show_photo_info(str(update.message))}', reply_markup=reply_markup)


def main():
    bot = Bot(token=TG_TOKEN, base_url=TG_API_URL)
    updater = Updater(token=TG_TOKEN, base_url=TG_API_URL, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    send_photo = MessageHandler(Filters.photo, get_photo)
    dispatcher.add_handler(send_photo)

    # send_video = MessageHandler(Filters.video, get_photo)
    # dispatcher.add_handler(send_video)
    #
    # send_audio = MessageHandler(Filters.audio, get_photo)
    # dispatcher.add_handler(send_audio)
    #
    # send_doc = MessageHandler(Filters.document, get_photo)
    # dispatcher.add_handler(send_doc)

    updater.dispatcher.add_handler(CallbackQueryHandler(button_save_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()