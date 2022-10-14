from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aioredis
from app.database import database
from app.router import users
from app.settings import settings

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
async def startup():
    await database.connect()
    app.state.db_redis = aioredis.from_url(settings.redis_host)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await app.state.db_redis.close()


app.include_router(users.router)
