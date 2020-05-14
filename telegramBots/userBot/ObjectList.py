import os, json
from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from typing import List, Dict

import buttons
from ApiConnection import ApiConnection
from config import Lang, reply_attachments
from ObjectMessage import ObjectMessage

class ObjectList():
    def __init__(self, connection: ApiConnection, 
                    data: str = '',
                    page: int = 0
                ):
        if data == '':
            self.list_all = True
        else:
            self.list_all = False
        self.data = data
        self.object_per_page = 10
        if self.list_all:
            self.items = connection.list_all()
        else:
            self.items : List[Dict] = connection.get_suggestions(data)
        self.connection = connection
        self.text = ""
        self.page = page
        self.available_pages = range(len(self.items) // self.object_per_page + 1)
        self.np = page + 1 if (page+1 in self.available_pages) else page
        self.pp = page - 1 if (page-1 in self.available_pages) else page
        if len(self.items) > 1:
            tmp = []
            offset = self.object_per_page*self.page
            for i, item in enumerate(self.items[0+offset:self.object_per_page+offset]):
                self.text += f"{offset+i+1}. {item['name']}\n"
                tmp.append(buttons.ObjectBtn(item['_id'], str(i+1+offset)))
            self.inline_kb = types.InlineKeyboardMarkup(row_width=5)
            self.inline_kb.row(*tmp[0:5])
            self.inline_kb.row(*tmp[5:10])
            self.inline_kb.row(
                buttons.PrevPage(self.data, self.pp),
                buttons.NextPage(self.data, self.np)
            )
            self.text += f"\nPage {page+1} of {self.available_pages[-1]+1}\n"
        else:
            self.inline_kb = None
        

    async def answer_to(self, message: types.Message):
        if len(self.items) == 0:
            await message.answer('Nothing found')
        elif len(self.items) == 1:
            await ObjectMessage(self.connection, self.items[0]['_id']).answer_to(message)
        else:
            await message.answer(self.text, reply_markup=self.inline_kb)            
    
    async def update_msg(self, message: types.Message):
        try:
            await message.edit_text(self.text, reply_markup=self.inline_kb)
        except MessageNotModified:
            # print(e)
            return
        