import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from telegramBots.media.fileManager import *
from telegramBots.initBot.config import TG_TOKEN
from telegramBots.initBot.config import TG_API_URL

# global variables keeps string information about telegram message
photo_info = ""
video_info = ""
audio_info = ""
document_info = ""


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Command /help - show bot commands\n"
                                  "Command /search - 'name of object to search in database' ")


def search(update, context):
    """ world search in all fields of the database """
    caption = update.message.text[8:]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Searching:\n"
             f"{str(caption)}")
    found_dict_list = search_all_by_word(str(caption))
    for file_dict in found_dict_list:
        if file_dict["attachments"][0]["content_type"].split('/')[0] == 'image':
            send_photo_from_dict(file_dict, context, update)
        elif file_dict["attachments"][0]["content_type"].split('/')[0] == 'audio':
            send_audio_from_dict(file_dict, context, update)
        elif file_dict["attachments"][0]["content_type"].split('/')[0] == 'video':
            send_video_from_dict(file_dict, context, update)


def send_photo_from_dict(photo_dict, context, update):
    try:
        with open(f"../../coreService/tests/content/images/{photo_dict['name']}", "rb") as file:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=file)
    except FileNotFoundError:
        print("No such file or directory")


def send_audio_from_dict(photo_dict, context, update):
    try:
        with open(f"../../coreService/tests/content/audios/{photo_dict['name']}", "rb") as file:
            context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=file)
    except FileNotFoundError:
        print("No such file or directory")


def send_video_from_dict(photo_dict, context, update):
    try:
        with open(f"../../coreService/tests/content/videos/{photo_dict['name']}", "rb") as file:
            context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=file)
    except FileNotFoundError:
        print("No such file or directory")


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your message is:\n"
             f"{update.message.text}"
    )


def button_save_files(update, context):
    global photo_info
    global video_info
    global audio_info
    global document_info
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))
    if query.data == "SavePhoto":
        print("Saving photo")
        if save_photo(photo_info):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Photo saved"
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Photo didn't save"
            )
        photo_info = ""
    if query.data == "SaveVideo":
        print("Saving video")
        if save_video(video_info):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Video saved"
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Video didn't save"
            )
        video_info = ""
    if query.data == "SaveAudio":
        print("Saving audio")
        if save_audio(audio_info):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Audio saved"
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Audio didn't save"
            )

        audio_info = ""
    if query.data == "SaveDocument":
        print("Saving document")
        if save_document(document_info):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Document saved"
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Document didn't save"
            )
        document_info = ""
    if query.data == "Cancel":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"File isn't saved"
        )


def get_photo(update, context):
    global photo_info
    photo_info = str(update.message)
    keyboard = [[InlineKeyboardButton("Save", callback_data='SavePhoto'),
                 InlineKeyboardButton("Cancel", callback_data='Cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'{show_photo_info(str(update.message))}', reply_markup=reply_markup)


def get_video(update, context):
    global video_info
    video_info = str(update.message)
    keyboard = [[InlineKeyboardButton("Save", callback_data='SaveVideo'),
                 InlineKeyboardButton("Cancel", callback_data='Cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'{show_video_info(str(update.message))}', reply_markup=reply_markup)


def get_audio(update, context):
    global audio_info
    audio_info = str(update.message)
    print(audio_info)
    keyboard = [[InlineKeyboardButton("Save", callback_data='SaveAudio'),
                 InlineKeyboardButton("Cancel", callback_data='Cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'{show_audio_info(str(update.message))}', reply_markup=reply_markup)


def get_document(update, context):
    global document_info
    document_info = str(update.message)
    print(document_info)
    keyboard = [[InlineKeyboardButton("Save", callback_data='SaveDocument'),
                 InlineKeyboardButton("Cancel", callback_data='Cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'{show_document_info(str(update.message))}', reply_markup=reply_markup)


def main():
    bot = Bot(token=TG_TOKEN, base_url=TG_API_URL)
    updater = Updater(token=TG_TOKEN, base_url=TG_API_URL, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    search_handler = CommandHandler('search', search)
    dispatcher.add_handler(search_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    send_photo = MessageHandler(Filters.photo, get_photo)
    dispatcher.add_handler(send_photo)

    send_video = MessageHandler(Filters.video, get_video)
    dispatcher.add_handler(send_video)

    send_audio = MessageHandler(Filters.audio, get_audio)
    dispatcher.add_handler(send_audio)

    send_doc = MessageHandler(Filters.document, get_document)
    dispatcher.add_handler(send_doc)

    updater.dispatcher.add_handler(CallbackQueryHandler(button_save_files))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
