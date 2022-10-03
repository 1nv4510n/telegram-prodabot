from aiogram import Router
from aiogram.types import TelegramObject
from bot.utils.logging import log

from aiogram.exceptions import TelegramForbiddenError

router = Router()

@router.errors()
async def forbidden_error_handler(update: TelegramObject, error: Exception) -> None:
    if isinstance(error, TelegramForbiddenError):
        log.warning(f'[{error}] Send default message error. Bot blocked by user.')
