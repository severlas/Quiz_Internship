from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.database import get_postgres_db
from app import models
from app.schemas.users import User, UserUpdateRequestModel, SignUpRequestModel, \
    UserJWT, TokenJWT, SignInRequestModel, UserPagination
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.settings import settings
from jose import jwt, JWTError
from log.config_log import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/sign-in')


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_postgres_db)
):
    user_data = UserService.verify_token(token=token)
    user = db.query(models.User).filter_by(id=user_data.id).first()
    return user


class UserService:
    """User services"""
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    def __init__(self, db: Session = Depends(get_postgres_db)):
        self.db = db

    """Create hash password"""
    @classmethod
    def create_hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    """Verify password"""
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

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
            print(user_data)
            id = user_data.get('id')

            if id is None:
                raise cls.auth_exception

        except JWTError:
            raise cls.auth_exception

        return UserJWT(id=id, email=user_data.get('email'))

    """Get list users"""
    @logger.catch
    def get_users(self, pagination: UserPagination) -> List[models.User]:
        users = self.db.query(models.User).limit(pagination.limit).offset(pagination.skip).all()
        return users

    """Protect method get user"""
    def _get_user(self, user_id: int) -> models.User:
        user = self.db.query(models.User).filter_by(id=user_id).first()

        if not user:
            logger.error(f'status: HTTP_404_NOT_FOUND, detail: User with id:{user_id} was not found')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with id:{user_id} was not found'
            )
        return user

    """Get user by id"""
    def get_user(self, user_id: int) -> models.User:
        return self._get_user(user_id)

    """Create user"""
    @logger.catch
    def create_user(self, user_data: SignUpRequestModel) -> models.User:
        hashed_password = self.create_hash_password(user_data.password)
        user_data.password = hashed_password
        user = models.User(**user_data.dict())
        self.db.add(user)
        self.db.commit()
        logger.info(f"User created successfully! 'data': {user_data.dict()}")
        return user

    """Update user data by id"""
    def update_user(self, user_id: int, user_data: UserUpdateRequestModel) -> models.User:
        user = self._get_user(user_id)
        for field, value in user_data:
            setattr(user, field, value)
        user.updated_at = datetime.now()
        self.db.commit()
        logger.info(f"User with id:{user_id} updated successfully! 'data': {user_data.dict()}")
        return user

    """Delete user by id"""
    def delete_user(self, user_id: int):
        user = self._get_user(user_id)
        self.db.delete(user)
        self.db.commit()
        logger.info(f"User with id:{user_id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    """Authenticate user by JWT token"""
    def sign_in(self, user_data: SignInRequestModel) -> TokenJWT:
        user = self.db.query(models.User).filter(models.User.email == user_data.email).first()

        if not user or not self.verify_password(user_data.password, user.password):
            logger.error('Could not validate credentials')
            raise self.auth_exception

        data_jwt = UserJWT(id=user.id, email=user.email)
        return self.create_token(data_jwt)
