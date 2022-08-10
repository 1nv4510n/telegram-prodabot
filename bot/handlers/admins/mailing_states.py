from aiogram.dispatcher.fsm.state import State, StatesGroup

class MailingStates(StatesGroup):
    edit_media = State()
    edit_text = State()
    button_text = State()
    button_url = State()