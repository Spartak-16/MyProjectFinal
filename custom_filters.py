from pyrogram import filters
from pyrogram.types import Message

def button_filter(button_text: str):
    async def func(flt, client, message: Message):
        return message.text == flt.button_text
    return filters.create(func, button_text=button_text)