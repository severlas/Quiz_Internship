from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.settings import settings
from redis_om import get_redis_connection
import databases

DATABASE_URL = "postgresql+asyncpg://" \
                          f"{settings.database_username}:" \
                          f"{settings.database_password}@" \
                          f"{settings.database_hostname}:" \
                          f"{settings.postgres_port}/" \
                          f"{settings.database_name}"

database = databases.Database(DATABASE_URL)

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=engine)


async def get_postgres_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
