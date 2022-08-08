from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import channels

def make_inline_keyboard(text: str, data: str, url_mode: bool = False) -> InlineKeyboardMarkup:
    if not url_mode:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=data)]])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, url=data)]])
    
def make_channels_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    for channel in channels:
        keyboard.row(InlineKeyboardButton(text=channel['name'], url=channel['join_link']))
        
    keyboard.row(InlineKeyboardButton(text='✅ Готово', callback_data='check_subscribe'))
    return keyboard.as_markup()