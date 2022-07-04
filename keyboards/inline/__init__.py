# inline
from aiogram import types


def inline_button(text, data) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text, callback_data=data)
