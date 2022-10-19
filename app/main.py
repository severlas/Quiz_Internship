from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aioredis
from app.database import database
from app.router import users, auth
from app.settings import settings
from log.config_log import logger

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@logger.catch
async def startup():
    await database.connect()
    app.state.db_redis = aioredis.from_url(settings.redis_host)
    logger.info('Application startup!')
    logger.info('Databases connection successfully!')


@app.on_event("shutdown")
@logger.catch
async def shutdown():
    await database.disconnect()
    await app.state.db_redis.close()
    logger.info('Application shutdown!')
    logger.info('Databases disconnect!')


app.include_router(users.router)
app.include_router(auth.router)
