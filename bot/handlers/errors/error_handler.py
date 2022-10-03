from aiogram import Router
from aiogram.types import TelegramObject
from bot.utils.logging import log

from aiogram.exceptions import TelegramForbiddenError
from aiogram.types.error_event import ErrorEvent

router = Router()

@router.errors()
async def forbidden_error_handler(error: ErrorEvent) -> None:
    if isinstance(error.exception, TelegramForbiddenError):
        log.warning(f'[{error.exception}] Send default message error. Bot blocked by user.')
