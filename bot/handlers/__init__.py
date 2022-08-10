from aiogram import Router

from .users import default, user_block
from .errors import error_handler
from .admins import admin_menu

router = Router()
router.include_router(default.router)
router.include_router(user_block.router)
router.include_router(error_handler.router)
router.include_router(admin_menu.router)