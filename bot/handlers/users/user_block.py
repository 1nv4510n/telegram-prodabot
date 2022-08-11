from aiogram import Router, F
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.logging import log
from bot.db.requests import is_user_exists, update_block_status

router = Router()
router.my_chat_member.filter(F.chat.type == 'private')

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession) -> None:
    if await is_user_exists(session, event.from_user.id):
        await update_block_status(session, event.from_user.id, True)
        log.info(f'User {event.from_user.first_name} blocked bot!')
    
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, session: AsyncSession) -> None:
    if await is_user_exists(session, event.from_user.id):
        await update_block_status(session, event.from_user.id, False)
        log.info(f'User {event.from_user.first_name} unblocked bot!')