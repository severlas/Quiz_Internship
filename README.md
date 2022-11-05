# Quiz

## Installation

1. Clone repository from GitHub
2. Create virtual environment (venv)
3. Install dependencies `pip install -r requirements.txt`
4. Create file `.env`
5. Add variable in file `.env`:
```

DATABASE_HOSTNAME='database host'
DATABASE_PASSWORD='postgres password'
DATABASE_NAME='postgres name'
DATABASE_USERNAME='postgres user'

POSTGRES_PORT='postgres port'
POSTGRES_PASSWORD='postgres password'
POSTGRES_DB='postgres name'

REDIS_PORT='redis port'
REDIS_PORTS='redis port for docker'
REDIS_HOST='redis host'

JWT_SECRET='JWT secret key'
JWT_ALGORITHM='JWT algorithm'
JWT_EXPIRATION='time expiration JWT'

DOMAIN='auth domain'
API_AUDIENCE='api application auth'
ISSUER='issuer auth'
ALGORITHM='algorithm'

TEST_DATABASE_NAME='name test database'

```
6. For make migrations run command `alembic revision --autogenarate -m "{name migrations}"`
7. For create tables in database run command `alembic upgrade head`
8. Run the app `uvicorn app.main:app` or with auto-reload `uvicorn app.main:app --reload`

## Set up PostgreSQL

1. [Read documentation about set up postgres](https://www.postgresql.org/download/)
2. Install postgres

## Set up Redis

1. [Read documentation about set up redis](https://redis.io/docs/getting-started/)
2. Install redis

## Run app with Docker
 
1. [Read documentation about set up docker](https://docs.docker.com/get-docker/)
2. Install docker
3. Run the command `docker-compose up --build`
4. For make migrations run command `docker-compose exec app alembic revision --autogenarate -m "{name migrations}"`
5. For create tables in database run command `docker-compose exec app alembic upgrade head`