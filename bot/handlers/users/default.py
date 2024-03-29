import asyncio
import random
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils import log
from bot.states import StatesList
from bot.config import config

from bot.db.requests import add_user, update_status
from bot.utils.helper import is_user_subscribed, get_release_text
from bot.keyboards.user_keyboard import make_inline_keyboard, make_channels_keyboard, make_chatgpt_keyboard

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    current_state = await state.get_state()
    if current_state == StatesList.waiting.state:
        await message.answer('🔥<b>Ожидайте получения фулла</b>🔥')
        await message.answer(
            "Попробуй нашего ChatGPT4 бота от Bing @chatgpt4_megabot",
            reply_markup=make_chatgpt_keyboard()
        )
    else:
        await state.set_state(StatesList.started)
        await add_user(session, message.from_user.id, message.from_user.first_name, StatesList.started._state)
        await message.answer(
            f'Привет, {message.from_user.first_name}! В этом боте тебя ждет продолжение видео с TikTok🔞\n\n<b>Попробуй нашего ChatGPT4 бота от Bing</b> @chatgpt4_megabot\n\nЖми на кнопку ниже 👇', 
            reply_markup=make_inline_keyboard('Получить продолжение🔞', 'start_callback')
        )
        log.info(f'User {message.from_user.first_name} started bot!')

@router.callback_query(StatesList.started, F.data == 'start_callback')
async def subscribe_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.set_state(StatesList.subscribe)
    await update_status(session, call.from_user.id, StatesList.subscribe._state)
    msg = await call.message.answer('Чтобы получить полное видео, <b>подпишитесь на наших спонсоров!</b>')
    await call.message.delete()
    await msg.answer('Подписаться:', reply_markup=make_channels_keyboard())

@router.callback_query(StatesList.subscribe, F.data == 'check_subscribe')
async def check_subscribe_handler(call: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    user_id = call.from_user.id
    if await is_user_subscribed(bot, user_id):
        await state.set_state(StatesList.waiting)
        await update_status(session, user_id, StatesList.waiting._state)
        await call.answer('Успешно!', show_alert=False)
        rel_time = random.randint(1, 4) if config.release_time == 'random' else int(config.release_time)
        msg = await call.message.answer(
            f'<b>Попробуй нашего ChatGPT4 бота от Bing</b> @chatgpt4_megabot\n\nИз-за большой нарузки, мы вышлем вам фулл через <b>{get_release_text(rel_time)}</b>\n⚠️<b>ЗА ЭТО ВРЕМЯ НЕЛЬЗЯ ОТПИСЫВАТЬСЯ ОТ СПОНСОРОВ!</b>⚠️',
            reply_markup=make_chatgpt_keyboard()    
        )
        await call.message.delete()
        await asyncio.sleep(rel_time * 60)
    
        if await is_user_subscribed(bot, user_id):
            await msg.delete()
            await bot.send_message(
                user_id, 
                '🔥 <b>ДЕРЖИ СВОЙ ФУЛЛ</b> 🔥', 
                reply_markup=make_inline_keyboard('🔥ФУЛЛ ЖМИ🔥', config.full_link, url_mode=True)
            )
            await update_status(session, user_id, 'subscribe_done')
            await state.clear()
        else:
            await msg.delete()
            await bot.send_message(
                user_id, 
                '⚠️\n<b>ВЫ ОТПИСАЛИСЬ ОТ СПОНСОРОВ\nПОВТОРИТЕ ПОДПИСКУ</b>\n⚠️',
                reply_markup=make_channels_keyboard()
            )
            await state.set_state(StatesList.subscribe)
            await update_status(session, user_id, StatesList.subscribe._state)
    else:
        await call.answer('Ошибка! Проверьте подписку.', show_alert=True)