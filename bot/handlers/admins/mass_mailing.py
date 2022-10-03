import asyncio
from typing import List
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ContentType, InlineKeyboardButton
from aiogram.filters import Text
import aiogram.exceptions as exceptions
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.logging import log
from bot.db.requests import get_mailing_users
from bot.keyboards.admin_keyboard import make_mailing_menu_keyboard, make_start_mailing_keyboard, make_admin_menu_keyboard

from .mailing_states import MailingStates

router = Router()

@router.callback_query(Text('mailing_menu'))
async def mass_mailing_menu_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MailingStates.mailing_state)
    await state.set_data(
        {
            'media_type' : ContentType.TEXT,
            'text' : 'Пример сообщения',
            'file_id' : None,
            'inline_markup' : InlineKeyboardBuilder()
        }
    )
    
    await call.message.edit_text(text='Выберите действие', reply_markup=make_mailing_menu_keyboard())
    
@router.callback_query(Text('back_mailing'))
async def back_mailing_menu_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MailingStates.mailing_state)
    await call.message.edit_text(text='Выберите действие', reply_markup=make_mailing_menu_keyboard())
    
@router.message(MailingStates.edit_media, Text('Отмена'))
@router.message(MailingStates.edit_text, Text('Отмена'))
@router.message(MailingStates.edit_button, Text('Отмена'))
async def back_mailing_menu_callback(message: Message, state: FSMContext) -> None:
    await state.set_state(MailingStates.mailing_state)
    await message.answer(text='Выберите действие', reply_markup=make_mailing_menu_keyboard())
      
@router.callback_query(MailingStates.mailing_state, Text('edit_text'))
async def edit_text_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(text="Введите текст рассылки. Либо напишите 'Отмена'")
    await state.set_state(MailingStates.edit_text)
    await call.message.delete()
  
@router.message(MailingStates.edit_text, F.text)
async def get_text_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.html_text)
    await state.set_state(MailingStates.mailing_state)
    await message.answer(text='<b>Успешно.</b>\nВыберите действие', reply_markup=make_mailing_menu_keyboard())
  
@router.callback_query(MailingStates.mailing_state, Text('edit_media'))
async def edit_media_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(text="Отправьте картинку/видео. Либо напишите 'Отмена'")
    await state.set_state(MailingStates.edit_media)
    await call.message.delete()
    
@router.message(MailingStates.edit_media, F.content_type.in_({'photo', 'video'}))
async def get_media_handler(message: Message, state: FSMContext) -> None:
    if message.photo:
        await state.update_data(file_id=message.photo[-1].file_id, media_type=ContentType.PHOTO)
    elif message.video:
        await state.update_data(file_id=message.video.file_id, media_type=ContentType.VIDEO)
    await state.set_state(MailingStates.mailing_state)
    await message.answer(text='<b>Успешно.</b>\nВыберите действие', reply_markup=make_mailing_menu_keyboard())

@router.callback_query(MailingStates.mailing_state, Text('add_button'))
async def add_button_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MailingStates.edit_button)
    await call.answer("Введите название, после URL кнопки через пробел! Либо напишите 'Отмена'", show_alert=True)
    await call.message.delete()
    
@router.message(MailingStates.edit_button, F.text)
async def edit_button_handler(message: Message, state: FSMContext) -> None:
    try:
        button = message.text.split(' ')
        if 'http://' not in button[1] and 'https://' not in button[1] and 'tg://' not in button[1]:
            raise ValueError
        current_data = await state.get_data()
        keyboard: InlineKeyboardBuilder = current_data['inline_markup']
        await state.update_data(
            inline_markup=keyboard.row(InlineKeyboardButton(text=button[0], url=button[1]))
        )
        await state.set_state(MailingStates.mailing_state)
        await message.answer(text='<b>Успешно.</b>\nВыберите действие', reply_markup=make_mailing_menu_keyboard())
    except IndexError:
        await message.answer("<b>Ошибка добавления кнопки</b>\nНазвание и ссылку должен отделять пробел! Либо напишите 'Отмена'\n")
    except ValueError:
        await message.answer("<b>Ошибка добавления кнопки</b>\nПроверьте написание ссылки! Либо напишите 'Отмена'\n")
    except Exception as e:
        await message.answer(f"<b>Ошибка добавления кнопки</b>\nПроверьте заполнение, либо напишите 'Отмена'\nИсключение:\n {e}")
        log.error(f'Add button ERROR. Exception: {e}')
        
@router.callback_query(MailingStates.mailing_state, Text('delete_button'))
async def delete_buttons_callback(call: CallbackQuery, state: FSMContext) -> None:
    try:
        await state.update_data(inline_markup=InlineKeyboardBuilder())
        await call.answer(text='Кнопки успешно удалены!', show_alert=True)
    except Exception as e:
        await call.message.answer(f'<b>Ошибка удаления кнопок! Исключение:\n{e}')
        log.error(f'Delete buttons ERROR. Exception: {e}')
        
@router.callback_query(MailingStates.mailing_state, Text('reset_post'))
async def reset_post_callback(call: CallbackQuery, state: FSMContext) -> None:
    try:
        await state.set_data(
            {
                'media_type' : ContentType.TEXT,
                'text' : 'Пример сообщения',
                'file_id' : None,
                'inline_markup' : InlineKeyboardBuilder()
            }
        )
        await call.answer(text='Пост успешно сброшен!', show_alert=True)
    except Exception as e:
        await call.message.answer(f'<b>Ошибка сброса поста! Исключение:\n{e}')
        log.error(f'Reset post ERROR. Exception: {e}')

async def post_preview(call: CallbackQuery, data: dict) -> None:
    if data['media_type'] == ContentType.VIDEO:
        await call.message.answer_video(
            video=data['file_id'],
            caption=data['text'],
            reply_markup=data['inline_markup'].as_markup()
        )
    elif data['media_type'] == ContentType.PHOTO:
        await call.message.answer_photo(
            photo=data['file_id'],
            caption=data['text'],
            reply_markup=data['inline_markup'].as_markup()
        )
    elif data['media_type'] == ContentType.TEXT:
        await call.message.answer(
            text=data['text'],
            reply_markup=data['inline_markup'].as_markup()
        )

@router.callback_query(MailingStates.mailing_state, Text('preview_post'))
async def preview_post_callback(call: CallbackQuery, state: FSMContext) -> None:
    current_data = await state.get_data()
    await post_preview(call, current_data)
    await call.message.answer(text='Выберите действие', reply_markup=make_mailing_menu_keyboard())
    await call.message.delete()
    
@router.callback_query(MailingStates.mailing_state, Text('start_mailing_menu'))
async def start_mailing_menu_callback(call: CallbackQuery, state: FSMContext) -> None:
    current_data = await state.get_data()
    if current_data['text'] != 'Пример сообщения':
        await post_preview(call, current_data)
        await call.message.answer('Вы уверены что хотите начать рассылку?', reply_markup=make_start_mailing_keyboard())
        await call.message.delete()
    else:
        await call.answer(text='Для рассылки необходимо создать пост', show_alert=True)
        
@router.callback_query(MailingStates.mailing_state, Text('start_mass_mailing'))
async def start_mass_mailing_callback(call: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    current_data = await state.get_data()
    spam_list: List[int] = [user.telegram_id for user in await get_mailing_users(session)]
    await call.message.answer(text=f'<b>Запуск рассылки, успешно!</b>\n\n Пользователей: {len(spam_list)}\nОжидаемое время рассылки {len(spam_list) * 2 + 20} секунд.')
    await call.message.edit_text('Выберите действие', reply_markup=make_admin_menu_keyboard())
    for chat_id in spam_list:
        try:
            match current_data['media_type']:
                case ContentType.PHOTO:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=current_data['file_id'],
                        caption=current_data['text'],
                        reply_markup=current_data['inline_markup'].as_markup()
                    )
                case ContentType.VIDEO:
                    await bot.send_video(
                        chat_id=chat_id,
                        video=current_data['file_id'],
                        caption=current_data['text'],
                        reply_markup=current_data['inline_markup'].as_markup()
                    )
                case ContentType.TEXT:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=current_data['text'],
                        reply_markup=current_data['inline_markup'].as_markup()
                    )
            await asyncio.sleep(2)
        except exceptions.TelegramForbiddenError:
            chat = await bot.get_chat(chat_id=chat_id)
            log.warning(f'Mailing send message error. User {chat.first_name} banned.')
        except exceptions.TelegramRetryAfter as e:
            log.error(f'Mailing send message Retry after: {e}')
        except exceptions.TelegramAPIError as e:
            log.error(f'Mailing send message Telegram API error: {e}')
        except exceptions.AiogramError as e:
            log.critical(f'Aiogram ERROR! {e}')
        
    await state.clear()
    