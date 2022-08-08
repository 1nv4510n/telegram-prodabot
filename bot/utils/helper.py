from aiogram import Bot
from aiogram.types import ChatMemberLeft

from bot.config import channels

async def is_user_subscribed(bot: Bot, telegram_id: int) -> bool:
    subscribe_pass = True
    for channel in channels:
        status = await bot.get_chat_member(channel['chat_id'], telegram_id)
        if isinstance(status, ChatMemberLeft):
            subscribe_pass = False
            
    return subscribe_pass

def get_release_text(time: int) -> str:
    text = f'{time} минут'
    if time == 1:
        return text + 'у'
    elif time in (2, 3, 4):
        return text + 'ы'
    else:
        return text