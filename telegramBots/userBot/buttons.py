import os, re, json
from  typing import List, Dict, Tuple, Union
from aiogram import  types


def more(_id: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton("⏬", callback_data=f"more:{_id}")

def less(_id: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton("⏬", callback_data=f"more:{_id}")

class More(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        super().__init__("⏬", callback_data=f"more:{_id}")

class Less(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        super().__init__("⏫", callback_data=f"less:{_id}")

class Lang_ru(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        super().__init__("🇷🇺", callback_data=f"lang:ru:{_id}")

class Lang_en(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        super().__init__("🇬🇧", callback_data=f"lang:en:{_id}")

class Attachment(types.InlineKeyboardButton):
    def __init__(self, _id: str, num: int, name: str = "📎"):
        super().__init__(name, callback_data=f"att:{_id}:{num}")

