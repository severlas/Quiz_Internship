from pydantic import BaseSettings


class Settings(BaseSettings):

    database_name: str
    database_username: str
    database_password: str
    database_hostname: str
    postgres_port: int

    redis_port: int
    redis_host: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expiration: int

    class Config:
        env_file = ".env"


settings = Settings()
