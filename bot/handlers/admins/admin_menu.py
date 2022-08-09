from aiogram import Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.filters.admin_filter import AdminFilter

from bot.keyboards.admin_keyboard import *

router = Router()
router.message.filter(AdminFilter(admin_id=config.admin_id))
router.callback_query.filter(AdminFilter(admin_id=config.admin_id))

@router.message(commands=['admin'])
async def admin_menu_handler(message: Message) -> None:
    await message.answer('Выберите действие', reply_markup=make_admin_menu_keyboard())
    
@router.callback_query(text='exit_menu')
async def exit_menu_callback(call: CallbackQuery) -> None:
    await call.message.delete()