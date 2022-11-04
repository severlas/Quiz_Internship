import pytest
from app.main import app
from app.models import BaseModel
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from app.database import get_postgres_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from app.settings import settings

DATABASE_URL_ASYNC = "postgresql+asyncpg://" \
                          f"{settings.database_username}:" \
                          f"{settings.database_password}@" \
                          f"{settings.database_hostname}:" \
                          f"{settings.postgres_port}/" \
                          f"test_quiz"

DATABASE_URL = "postgresql://" \
                          f"{settings.database_username}:" \
                          f"{settings.database_password}@" \
                          f"{settings.database_hostname}:" \
                          f"{settings.postgres_port}/" \
                          f"test_quiz"


async_engine = create_async_engine(DATABASE_URL_ASYNC, poolclass=NullPool)
engine = create_engine(DATABASE_URL)
TestSessionLocal = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=async_engine)


@pytest.fixture()
async def get_test_db() -> AsyncSession:
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    async with TestSessionLocal() as db:
        yield db


# @pytest.fixture()
# async def client(get_test_db):
#     async def test_db():
#         try:
#             yield get_test_db
#         finally:
#             await get_test_db.close()
#     app.dependency_overrides[get_postgres_db] = test_db
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac
