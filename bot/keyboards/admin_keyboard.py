from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def make_admin_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='✉️ Рассылка', callback_data='mailing_menu'),
        InlineKeyboardButton(text='📊 Статистика', callback_data='statistics')
    )
    # keyboard.row(
    #     InlineKeyboardButton(text='✔️ Добавить канал', callback_data='add_channel'),
    #     InlineKeyboardButton(text='❌ Удалить канал', callback_data='remove_channel')
    # )
    keyboard.row(InlineKeyboardButton(text='🚫 Выход', callback_data='exit_menu'))
    
    return keyboard.as_markup()

def make_statistics_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='⬅️ Назад', callback_data='back_menu')
    keyboard.button(text='♻️ Сбросить подписки', callback_data='reset_subscribed')
    return keyboard.as_markup()

def make_mailing_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='📜 Изменить текст', callback_data='edit_text'),
        InlineKeyboardButton(text='📷 Изменить медиа', callback_data='edit_media')
    )
    keyboard.row(
        InlineKeyboardButton(text='▶️ Добавить кнопку', callback_data='add_button'),
        InlineKeyboardButton(text='⏹️ Удалить кнопки', callback_data='delete_button')
    )
    keyboard.row(
        InlineKeyboardButton(text='📢 Посмотреть пост', callback_data='preview_post'),
        InlineKeyboardButton(text='🗑️ Сбросить пост', callback_data='reset_post')
    )
    keyboard.row(InlineKeyboardButton(text='✈️ Начать рассылку', callback_data='start_mailing_menu'))
    keyboard.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back_menu'))
    return keyboard.as_markup()

def make_start_mailing_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='⬅️ Назад', callback_data='back_mailing'),
        InlineKeyboardButton(text='🆗 НАЧАТЬ', callback_data='start_mass_mailing')
    )
    return keyboard.as_markup()