from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from redis_om import get_redis_connection
import databases

DATABASE_URL = "postgresql://" \
                          f"{settings.database_username}:" \
                          f"{settings.database_password}@" \
                          f"{settings.database_hostname}:" \
                          f"{settings.database_port}/" \
                          f"{settings.database_name}"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


redis_db = get_redis_connection(
    host=settings.database_hostname,
    port=settings.redis_port
)
