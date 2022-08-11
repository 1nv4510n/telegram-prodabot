from aiogram.dispatcher.fsm.state import State, StatesGroup

class MailingStates(StatesGroup):
    mailing_state = State()
    edit_media = State()
    edit_text = State()
    edit_button = State()