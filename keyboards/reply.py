# reply
from aiogram import types

from config.text_util import SAVE_POST


def remove() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def save():
    return types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(SAVE_POST)
