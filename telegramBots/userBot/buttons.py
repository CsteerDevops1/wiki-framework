import os, re, json
from  typing import List, Dict, Tuple, Union
from aiogram import  types


class More(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        cd = f"more:{_id}"
        assert len(cd.encode()) < 64
        super().__init__("⏬", callback_data=cd)

class Less(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        cd = f"less:{_id}"
        assert len(cd.encode()) < 64
        super().__init__("⏫", callback_data=cd)

class Lang_ru(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        cd = f"lang:ru:{_id}"
        assert len(cd.encode()) < 64
        super().__init__("🇷🇺", callback_data=cd)

class Lang_en(types.InlineKeyboardButton):
    def __init__(self, _id: str):
        cd = f"lang:en:{_id}"
        assert len(cd.encode()) < 64
        super().__init__("🇬🇧", callback_data=cd)

class Attachment(types.InlineKeyboardButton):
    def __init__(self, _id: str, num: int, name: str = "📎"):
        cd = f"att:{_id}:{num}"
        assert len(cd.encode()) < 64
        super().__init__(name, callback_data=cd)

class LinkToEditBot(types.InlineKeyboardButton):
    def __init__(self, _id: str, name: str = "edit in @cs_wiki_edit_bot"):
        # link = f"tg://cs_wiki_edit_bot?start={_id}"
        link = f"https://t.me/cs_wiki_edit_bot?start={_id}"
        super().__init__(name, url=link)
