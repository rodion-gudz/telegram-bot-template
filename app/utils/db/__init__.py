from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


async def init(database_engine: str):
    from app.common import DB

    from .base import Base

    engine = create_async_engine(database_engine, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return sessionmaker(engine, expire_on_commit=False, class_=DB)
