from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# 512MB'lık tek instance VPS: tek uvicorn worker'ı besleyen küçük bir pool
# yeterli, varsayılan (5+10 overflow) burada gereksiz RAM/bağlantı israfı.
engine = create_async_engine(settings.database_url, pool_pre_ping=True, pool_size=5, max_overflow=2)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
