from aiogram import types

import filters
from data import config
from keyboards.inline import inline_button


def in_chat_inline_keyboard(event_id: int, sender_chat_id: str, receiver_chat_id: str,
                            current_event_id) -> types.InlineKeyboardButton:
    """
    send inline keyboard if user not in chat
    :param event_id: event id
    :param sender_chat_id: chat id of sender
    :param receiver_chat_id: chat id of owner event
    :param current_event_id: check that message from same user
    :return: types.InlineKeyboardButton
    """
    if not filters.filters.user_in_chat(receiver_chat_id=receiver_chat_id,
                                        sender_chat_id=sender_chat_id):
        return types.InlineKeyboardMarkup(). \
            add(
            inline_button(config.EVENT_ANSWER, f'{config.CONNECT_TO_CHAT}:{event_id}:{sender_chat_id}'),
            inline_button(config.SHOW_EVENT_IN_CHAT, f'{config.SHOW_EVENT_MARKER}:{event_id}')
        )
