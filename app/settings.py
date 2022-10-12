from pydantic import BaseSettings


class Settings(BaseSettings):

    database_name: str
    database_username: str
    database_password: str
    database_hostname: str
    postgres_port: int

    redis_port: int

    class Config:
        env_file = ".env"


settings = Settings()
