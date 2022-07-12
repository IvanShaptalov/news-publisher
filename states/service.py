from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesGroup(StatesGroup):
    edit_state = State()
    text_entered_state = State()
