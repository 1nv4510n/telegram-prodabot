from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.logging import log
from bot.keyboards.admin_keyboard import make_mailing_menu_keyboard

from .mailing_states import MailingStates
from .admin_menu import router

@router.callback_query(text='mailing_menu')
async def mass_mailing_menu_callback(call: CallbackQuery) -> None:
    await call.message.edit_text(text='Выберите действие', reply_markup=make_mailing_menu_keyboard())