from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.misc.database import async_session_maker
from src.config.settings import settings

import logging
logger = logging.getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
