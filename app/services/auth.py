from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt, JWTError
from log.config_log import logger
from app.database import get_postgres_db
from app.settings import settings
from app.models.users import UserModel
from app.schemas.users import UserJWT, TokenJWT, SignUpRequestModel, SignInRequestModel
from app.services.hash_password_helper import HashPasswordHelper
from app.services.verify_token import VerifyToken
from app.services.users import UserService
from app.services.exceptions import AuthenticateError

auth0_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/sign-in')


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        token_auth: str = Depends(auth0_scheme),
        db: AsyncSession = Depends(get_postgres_db),
        service: UserService = Depends()
) -> UserModel:

    payload = VerifyToken(token_auth.credentials).verify()
    user_email = payload.get('email')

    if user_email is None:
        user_data = AuthService.verify_token(token=token)
        user = await db.execute(select(UserModel).filter_by(id=user_data.id))
        user = user.scalar()
        return user

    user = await db.execute(select(UserModel).filter_by(email=user_email))
    user = user.scalar()

    if not user:
        user_data = SignUpRequestModel(
            email=user_email,
            username=user_email[:user_email.index('@')],
            password=f'{user_email}{datetime.now()}'
        )
        user = await service.create_user(user_data=user_data)
    return user


class AuthService:
    """Authenticate service"""

    """Create JWT token"""
    @classmethod
    def create_token(cls, user_data: UserJWT) -> TokenJWT:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_expiration
        )
        payload = {
            'exp': expire,
            'user': user_data.dict()
        }
        jwt_token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        logger.info(f'User with id:{user_data.id} Authenticated successfully!')
        return TokenJWT(access_token=jwt_token)

    """Verify JWT token"""
    @classmethod
    def verify_token(cls, token: str) -> UserJWT:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.jwt_secret,
                algorithms=settings.jwt_algorithm
            )
            user_data = payload.get('user')
            id = user_data.get('id')

            if id is None:
                raise AuthenticateError

        except JWTError:
            raise AuthenticateError

        return UserJWT(id=id, email=user_data.get('email'))

    def __init__(self, db: AsyncSession = Depends(get_postgres_db)):
        self.db = db

    """Authenticate user by email and password"""
    async def sign_in(self, user_data: SignInRequestModel) -> TokenJWT:
        user = await self.db.execute(select(UserModel).filter_by(email=user_data.email))
        user = user.scalar()

        if not user or not HashPasswordHelper.verify_password(user_data.password, user.password):
            raise AuthenticateError

        data_jwt = UserJWT(id=user.id, email=user.email)
        return self.create_token(data_jwt)
