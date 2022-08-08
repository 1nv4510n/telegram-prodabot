from typing import Dict, List
from contextlib import suppress

from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from bot.db.models import UsersEntry

# get data

async def is_user_exists(session: AsyncSession, telegram_id: int) -> bool:
    request = await session.execute(
        select(UsersEntry).filter_by(telegram_id=telegram_id)
    )
    return request.scalars().first() is not None

# modify data

async def add_user(session: AsyncSession, telegram_id: int, name: str, status: str) -> None:
    entry = UsersEntry()
    entry.telegram_id = telegram_id
    entry.name = name
    entry.status = status
    entry.blocked = False
    session.add(entry)
    with suppress(IntegrityError):
        await session.commit()
        
async def update_status(session: AsyncSession, telegram_id: int, status: str) -> None:
    await session.execute(
        update(UsersEntry).where(UsersEntry.telegram_id == telegram_id).values(status=status)
    )
    with suppress(IntegrityError):
        await session.commit()
        
async def update_block_status(session: AsyncSession, telegram_id: int, blocked: bool) -> None:
    await session.execute(
        update(UsersEntry).where(UsersEntry.telegram_id == telegram_id).values(blocked=blocked)
    )
    with suppress(IntegrityError):
        await session.commit()