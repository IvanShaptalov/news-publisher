from aiogram import types

from data import config
from keyboards.reply import default_reply_markup


def remove() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def exit_from_chat_or_show_event() -> types.ReplyKeyboardMarkup:
    return default_reply_markup().add(config.EXIT_FROM_CHAT)
