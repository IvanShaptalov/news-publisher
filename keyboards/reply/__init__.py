# reply
from aiogram import types


def default_reply_markup(resize_keyboard=True, selective=True) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)