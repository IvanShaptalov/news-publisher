from aiogram import types
from aiogram.dispatcher import FSMContext


async def send_text_message(message: types.Message, state: FSMContext):  # create class to send all type of data
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        chat_id = data['sender_chat_id']
        sender = messenger.TextSender(event_id=event_id,
                                      sender_id=chat_id)
        await sender.forward_data(message)


async def send_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        chat_id = data['sender_chat_id']
        sender = messenger.PhotoSender(event_id=event_id,
                                       sender_id=chat_id)
        await sender.forward_data(message)


async def send_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        chat_id = data['sender_chat_id']
        sender = messenger.VideoSender(event_id=event_id,
                                       sender_id=chat_id)
        await sender.forward_data(message)
