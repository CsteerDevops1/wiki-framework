import os, json
from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

import buttons
from ApiConnection import ApiConnection
from config import Lang, reply_attachments

class ObjectMessage():
    def __init__(self, connection: ApiConnection, 
                _id: str, 
                expanded: bool = False,
                lang: Lang = Lang.ENG):
        self._id = _id
        self.data = connection.get_object(_id)
        self.text = ""
        collapse_btn = buttons.Less(self._id) if expanded else buttons.More(self._id)
        lang_btn = buttons.Lang_ru(self._id) if lang == Lang.ENG else buttons.Lang_en(self._id)
        if lang == Lang.ENG:
            self.text += f"{self.data['name']}\n"
            self.text += f"{self.data['description']}\n\n"
        elif lang == Lang.RUS:
            self.text += f"{self.data['russian_name']}\n"
            self.text += f"{self.data['russian_description']}\n\n"
        self.inline_kb = types.InlineKeyboardMarkup(row_width=5)
        if expanded:
            self.text += f"id: {self.data['_id']}\n"
            if self.data['text'] != '':
                self.text += f"Text: {self.data['text']}\n"
            if len(self.data['relations']) != 0:
                self.text += f"Relations: {','.join(self.data['relations'])}\n"
            if len(self.data['synonyms']) != 0:
                self.text += f"Synonyms: {','.join(self.data['synonyms'])}\n"
            if len(self.data['tags']) != 0:
                self.text += f"Tags: {','.join(['#'+x for x in self.data['tags']])}\n"
            self.text += f"Created: {self.data['creation_date']}\n"
        self.inline_kb.row(collapse_btn, lang_btn)
        for i, attachment in enumerate(self.data['attachments']):
            self.inline_kb.add(
                buttons.Attachment(
                    _id=self._id, 
                    num=i, 
                    name=attachment['content_type'].split('/')[1]
                )
            )
        self.inline_kb.row(buttons.LinkToEditBot(_id))
    
    async def answer_to(self, message: types.Message):
        await message.answer(self.text, reply_markup=self.inline_kb)
    
    async def update_msg(self, message: types.Message):
        try:
            await message.edit_text(self.text, reply_markup=self.inline_kb)
        except MessageNotModified as e:
            print(e)
        
    async def reply_attachment(self, num: int,  message: types.Message):
        try:
            attachment = self.data['attachments'][num]
        except BaseException as e:
            print('No such attachment:', f"{self._id}:{num}")
            print(e)
            return
        await reply_attachments(message, [attachment,])
        