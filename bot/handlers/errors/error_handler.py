from aiogram import Router
from aiogram.types import TelegramObject
from bot.utils.logging import log

from aiogram.exceptions import TelegramForbiddenError

router = Router()

@router.errors()
async def forbidden_error_handler(update: TelegramObject, exception: Exception) -> None:
    if isinstance(exception, TelegramForbiddenError):
        log.warning(f'[{exception}] Send default message error. Bot blocked by user.')
