from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from log.config_log import logger
from app.database import get_postgres_db
from app.settings import settings
from app import models
from app.schemas.users import UserJWT, TokenJWT, SignUpRequestModel, SignInRequestModel
from app.services.hash_password_helper import HashPasswordHelper
from app.services.verify_token import VerifyToken
from app.services.users import UserService

auth0_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/sign-in')


def get_current_user(
        token: str = Depends(oauth2_scheme),
        token_auth: str = Depends(auth0_scheme),
        db: Session = Depends(get_postgres_db)
) -> models.User:

    payload = VerifyToken(token_auth.credentials).verify()
    user_email = payload.get('email')

    if user_email is None:
        user_data = AuthService.verify_token(token=token)
        user = db.query(models.User).filter_by(id=user_data.id).first()
        return user

    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        user_data = SignUpRequestModel(
            email=user_email,
            username=user_email[:user_email.index('@')],
            password=f'{user_email}{datetime.now()}'
        )
        UserService.create_user(user_data=user_data)
    return user


class AuthService:

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

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
                raise cls.auth_exception

        except JWTError:
            raise cls.auth_exception

        return UserJWT(id=id, email=user_data.get('email'))

    def __init__(self, db: Session = Depends(get_postgres_db)):
        self.db = db

    """Authenticate user by email and password"""
    def sign_in(self, user_data: SignInRequestModel) -> TokenJWT:
        user = self.db.query(models.User).filter(models.User.email == user_data.username).first()

        if not user or not HashPasswordHelper.verify_password(user_data.password, user.password):
            logger.error('Could not validate credentials')
            raise self.auth_exception

        data_jwt = UserJWT(id=user.id, email=user.email)
        return self.create_token(data_jwt)
