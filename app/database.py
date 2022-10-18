from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from redis_om import get_redis_connection
import databases

DATABASE_URL = "postgresql://" \
                          f"{settings.database_username}:" \
                          f"{settings.database_password}@" \
                          f"{settings.database_hostname}:" \
                          f"{settings.postgres_port}/" \
                          f"{settings.database_name}"

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
