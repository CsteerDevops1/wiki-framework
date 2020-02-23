'''
https://api.telegram.org/bot1069387829:AAGBFSPsq2q1o_TfEIAo4ay0GsU_0QWJWnE/getFile?file_id=AgACAgIAAxkBAAPNXk8H2oXQ7NnbFoV9HW_7mNBglToAAs6sMRsl5nhKOKnJ6ikTZTccKHeRLgADAQADAgADbQADzB4AAhgE

https://api.telegram.org/bot1069387829:AAGBFSPsq2q1o_TfEIAo4ay0GsU_0QWJWnE/getFile?file_id=AgACAgIAAxkBAAPHXk71qOnjb0d7KhagxI8xcqVyQ-EAArisMRt0hXlKe0Ysv6r6eaA2dVwPAAQBAAMCAAN5AANpyAUAARgE

https://api.telegram.org/file/bot1069387829:AAGBFSPsq2q1o_TfEIAo4ay0GsU_0QWJWnE/photos/file_0.jpg
https://api.telegram.org/file/bot1069387829:AAGBFSPsq2q1o_TfEIAo4ay0GsU_0QWJWnE/photos/file_1.jpg
'''

import os
import requests
from PIL import Image, ExifTags
from telegramBots.initBot.config import TG_TOKEN

file = "AgACAgIAAxkBAAPLXk8DGnp7lwABNJNErRG4sNm5KHz9AALOrDEbJeZ4SjipyeopE2U3HCh3kS4AAwEAAwIAA20AA8weAAIYBA"
d = {'message_id': 199, 'date': 1582233000,
     'chat': {'id': 108772385, 'type': 'private', 'username': 'borsukl', 'first_name': 'Liza', 'last_name': 'Borsuk'},
     'entities': [], 'caption_entities': [], 'photo': [
        {'file_id': 'AgACAgIAAxkBAAPHXk71qOnjb0d7KhagxI8xcqVyQ-EAArisMRt0hXlKe0Ysv6r6eaA2dVwPAAQBAAMCAANtAANsyAUAARgE',
         'width': 200, 'height': 320, 'file_size': 22713},
        {'file_id': 'AgACAgIAAxkBAAPHXk71qOnjb0d7KhagxI8xcqVyQ-EAArisMRt0hXlKe0Ysv6r6eaA2dVwPAAQBAAMCAAN4AANryAUAARgE',
         'width': 499, 'height': 800, 'file_size': 97164},
        {'file_id': 'AgACAgIAAxkBAAPHXk71qOnjb0d7KhagxI8xcqVyQ-EAArisMRt0hXlKe0Ysv6r6eaA2dVwPAAQBAAMCAAN5AANpyAUAARgE',
         'width': 798, 'height': 1280, 'file_size': 178124}], 'new_chat_members': [], 'new_chat_photo': [],
     'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False,
     'channel_chat_created': False,
     'from': {'id': 108772385, 'first_name': 'Liza', 'is_bot': False, 'last_name': 'Borsuk', 'username': 'borsukl',
              'language_code': 'ru'}}
# def width_height(photoPath):
#     large = d["photo"][-1:]
#     print(large[0]["file_id"])
#     print(large[0]["width"])
#     print(large[0]["height"])
#     print(large[0]["file_size"])
#
#
#
#
#
#
# width_height(d)
img = "https://api.telegram.org/file/bot1069387829:AAGBFSPsq2q1o_TfEIAo4ay0GsU_0QWJWnE/photos/file_0.jpg"
p = requests.get(img)
out = open("photos/img.jpg", "wb")
out.write(p.content)
out.close()
