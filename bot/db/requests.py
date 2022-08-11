from typing import Dict, List, Optional
from contextlib import suppress
from urllib import request

from sqlalchemy import select, update, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from bot.db.models import UsersEntry

# get data

async def get_users_count(session: AsyncSession) -> Optional[int]:
    request = await session.execute(
        select(func.count()).select_from(
            select(UsersEntry).distinct(UsersEntry.telegram_id).subquery()
        )
    )
    return request.scalar()

async def get_blocked_users(session: AsyncSession) -> Optional[int]:
    request = await session.execute(
        select(func.count()).select_from(
            select(UsersEntry).where(UsersEntry.blocked == True).subquery()
        )
    )
    return request.scalar()

async def get_subscribed_users(session: AsyncSession) -> Optional[int]:
    request = await session.execute(
        select(func.count()).select_from(
            select(UsersEntry).where(UsersEntry.status == 'subscribe_done').subquery()
        )
    )
    return request.scalar()

async def is_user_exists(session: AsyncSession, telegram_id: int) -> bool:
    request = await session.execute(
        select(UsersEntry).filter_by(telegram_id=telegram_id)
    )
    return request.scalars().first() is not None

async def get_mailing_users(session: AsyncSession) -> List[UsersEntry]:
    searching_data = await session.execute(
        select(UsersEntry).where(UsersEntry.blocked == False)
    )
    
    return searching_data.scalars().all()

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
        
async def reset_subscribed_users(session: AsyncSession) -> None:
    await session.execute(
        update(UsersEntry).values(status="started")
    )
    await session.commit()