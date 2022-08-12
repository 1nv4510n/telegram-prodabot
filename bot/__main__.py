from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from magic_filter import F
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import config
from .commands import set_commands

from .db.base import Base
from .middlewares import DbSessionMiddleware
from .utils import log

from . import handlers

async def main():
    engine = create_async_engine(config.postgres_dsn, future=True, echo=False)

    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # FIRST LAUNCH
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    
    if config.bot_fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))
        
    dp.message.filter(F.chat.type == 'private')
    
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))
    dp.my_chat_member.middleware(DbSessionMiddleware(db_pool))

    dp.include_router(handlers.router)

    await set_commands(bot)
    
    try:
        log.info('BOT STARTED')
        await dp.start_polling(bot, polling_timeout=60)
    except Exception as e:
        log.error(f'BOT START ERROR: {e}')
    finally:
        log.info('BOT STOPPED')
        await bot.session.close()