from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.filters import Text
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.logging import log
from bot.db.requests import get_users_count, get_blocked_users, get_subscribed_users, reset_subscribed_users
from bot.keyboards.admin_keyboard import make_statistics_keyboard

router = Router()

@router.callback_query(Text('statistics'))
async def show_statistics_callback(call: CallbackQuery, session: AsyncSession) -> None:
    stats = {
        'total_users' : await get_users_count(session),
        'blocked_users' : await get_blocked_users(session),
        'subscribed_users' : await get_subscribed_users(session)
    }
    if not stats['total_users'] == 0:
        if stats['blocked_users'] == stats['total_users']:
            stats['blocked_percent'] = 100
        else:
            stats['blocked_percent'] = round(stats['blocked_users'] / stats['total_users'] * 100)
            
        if stats['subscribed_users'] == stats['total_users']:
            stats['subscribed_percent'] = 100
        else:
            stats['subscribed_percent'] = round(stats['subscribed_users'] / stats['total_users'] * 100)
    else:
        stats['blocked_percent'] = 0
        stats['subscribed_percent'] = 0
        
    text = (
        f"👨 <b>Всего пользователей:</b> {stats['total_users']}\n"
        f"✅ <b>Активных:</b> {stats['total_users'] - stats['blocked_users']}\n"
        f"❌ <b>Забанили:</b> {stats['blocked_users']}\n"
        f"💯 <b>Процент забаненных:</b> {stats['blocked_percent']} %\n\n"
        f"💋 <b>Подписок:</b> {stats['subscribed_users']}\n"
        f"💌 <b>Процент подписок:</b> {stats['subscribed_percent']} %"
    )
    
    await call.message.edit_text(text=text, reply_markup=make_statistics_keyboard())
    
@router.callback_query(Text('reset_subscribed'))
async def reset_subscribed_callback(call: CallbackQuery, session: AsyncSession) -> None:
    try:
        await reset_subscribed_users(session)
        await call.answer(text='Сброс статусов. Успешно!', show_alert=True)
        log.info('Reset users status. Successful!')
    except Exception as e:
        await call.message.answer(f'<b>Исключение:</b> \n\n{e}')
        await call.answer(text='Ошибка сброса статусов!', show_alert=True)
        log.error(f'Reset users status ERROR. Exception: {e}')