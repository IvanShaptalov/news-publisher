import datetime

from aiogram import types, Bot
from aiogram.types import PhotoSize


def get_full_user_name(message: types.Message) -> str:
    """get user fullname from message"""
    if message.from_user:
        pre_fn = message.from_user.first_name
        pre_ln = message.from_user.last_name
        first_name = pre_fn if pre_fn else ' '
        last_name = pre_ln if pre_ln else ' '
        return f'{first_name} {last_name}'
    else:
        return ''


def retrieve_message_unique_id(message: types.Message, bot: Bot):
    photo = message.photo[0]
    assert isinstance(photo, PhotoSize)
    photo_file_id = photo.file_id
    return photo_file_id



def get_id_from_data(data: str, index):
    """
    get id from data
    :param data: data from callback
    :param index: index of information
    """
    assert ':' in data
    return data.split(':')[index]