from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.config import TOKEN


bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
