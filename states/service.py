from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesGroup(StatesGroup):
    text_entered_state = State()
