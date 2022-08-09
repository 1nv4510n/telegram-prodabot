from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def make_admin_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='✉️ Рассылка', callback_data='send_out'),
        InlineKeyboardButton(text='📊 Статистика', callback_data='statistics')
    )
    # keyboard.row(
    #     InlineKeyboardButton(text='✔️ Добавить канал', callback_data='add_channel'),
    #     InlineKeyboardButton(text='❌ Удалить канал', callback_data='remove_channel')
    # )
    keyboard.row(InlineKeyboardButton(text='🚫 Выход', callback_data='exit_menu'))
    
    return keyboard.as_markup()