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

    domain: str
    api_audience: str
    issuer: str
    algorithm: str

    test_database_name: str
    test_database_hostname: str

    email_host: str
    email_host_sender: str
    email_host_password: str
    email_port: int


    class Config:
        env_file = ".env"


settings = Settings()
