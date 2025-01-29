from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton

from data.texts import button
def reply_keyboards(lang="uz", *args):
    return [KeyboardButton(text=button(i, lang)) for i in args]
