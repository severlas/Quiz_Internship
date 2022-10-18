from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Union
from app.database import get_postgres_db
from app import models
from app.schemas.users import User, UserUpdateRequestModel, SignUpRequestModel, UserPagination
from datetime import datetime, timedelta
from app.settings import settings
from log.config_log import logger
from app.services.hash_password_helper import HashPasswordHelper


class UserService:
    """User services"""

    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f'Not authorized to perform requested action'
    )
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with id:{id} was not found'
    )

    def __init__(self, db: Session = Depends(get_postgres_db)):
        self.db = db

    """Get list users"""
    def get_users(self, user_id: int, pagination: UserPagination) -> List[models.User]:
        user = self.db.query(models.User).filter_by(id=user_id, is_admin=True).first()

        if user is None:
            logger.error(f'status: HTTP_403_NOT_FORBIDDEN, detail: Not authorized to perform requested action')
            raise self.forbidden_exception

        users = self.db.query(models.User).limit(pagination.limit).offset(pagination.skip).all()
        return users

    """Protect method get user"""
    def _get_user(self, id: int) -> models.User:
        user = self.db.query(models.User).filter_by(id=id).first()

        if not user:
            logger.error(f'status: HTTP_404_NOT_FOUND, detail: User with id:{id} was not found')
            raise self.not_found_exception
        return user

    """Get user by id"""
    def get_user(self, id: int, user_id: int) -> models.User:
        if id != user_id:
            logger.error(f'status: HTTP_403_NOT_FORBIDDEN, detail: Not authorized to perform requested action')
            raise self.forbidden_exception
        return self._get_user(id)

    """Create user"""
    @logger.catch
    def create_user(self, user_data: SignUpRequestModel) -> models.User:
        hashed_password = HashPasswordHelper.create_hash_password(user_data.password)
        user_data.password = hashed_password
        user = models.User(**user_data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User created successfully! 'data': {user_data.dict()}")
        return user

    """Update user data by id"""
    def update_user(self, id: int, user_id: int, user_data: UserUpdateRequestModel) -> models.User:
        if id != user_id:
            logger.error(
                f'status: HTTP_403_NOT_FORBIDDEN, '
                f'detail: User with id:{user_id} wanted to update user data with id:{id}'
            )
            raise self.forbidden_exception
        user = self.db.query(models.User).filter_by(id=id)

        if not user.first():
            logger.error(f'status: HTTP_404_NOT_FOUND, detail: User with id:{id} was not found')
            raise self.not_found_exception

        if user_data.password:
            hashed_password = HashPasswordHelper.create_hash_password(user_data.password)
            user_data.password = hashed_password

        user.update(user_data.dict(exclude_unset=True))
        user = user.first()
        user.update = datetime.now()
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User with id:{id} updated successfully! 'data': {user_data.dict(exclude_unset=True)}")
        return user

    """Delete user by id"""
    def delete_user(self, id: int, user_id: int):
        if id != user_id:
            logger.error(
                f'status: HTTP_403_NOT_FORBIDDEN, '
                f'detail: User with id:{user_id} wanted to delete user with id:{id}!'
            )
            raise self.forbidden_exception
        user = self._get_user(id)
        self.db.delete(user)
        self.db.commit()
        logger.info(f"User with id:{id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
