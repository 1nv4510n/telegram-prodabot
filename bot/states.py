from aiogram.fsm.state import State, StatesGroup

class StatesList(StatesGroup):
    started = State()
    subscribe = State()
    waiting = State()