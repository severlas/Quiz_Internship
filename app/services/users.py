from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
from typing import List, Optional, Union
from app.database import get_postgres_db
from app.models.users import UserModel
from app.schemas.users import User, UserUpdateRequestModel, SignUpRequestModel, UserDetail
from app.schemas.paginations import UserPagination
from datetime import datetime, timedelta
from app.settings import settings
from log.config_log import logger
from app.services.hash_password_helper import HashPasswordHelper
from app.services.exceptions import NotFoundError, PermissionError
from app.services.baseservice import BaseService


class UserService(BaseService):
    """User CRUD"""

    """Get list users"""
    async def get_users(self, pagination: UserPagination) -> List[UserModel]:
        users = await self.db.execute(select(UserModel).limit(pagination.limit).offset(pagination.skip))
        users = users.scalars().all()
        return users

    """Get user by id"""
    async def get_user(self, id: int) -> UserDetail:
        user = await self._get_user_by_id(id)
        requests = await self._get_requests_by_user_id(id)
        user_data = UserDetail(
            **user.__dict__,
            requests=requests
        )
        return user_data

    """Create user"""
    @logger.catch
    async def create_user(self, user_data: SignUpRequestModel) -> UserModel:
        hashed_password = HashPasswordHelper.create_hash_password(user_data.password)
        user_data.password = hashed_password
        user = UserModel(**user_data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        logger.info(f"User created successfully! 'data': {user_data.dict()}")
        return user

    """Update user data by id"""
    async def update_user(self, id: int, user_id: int, user_data: UserUpdateRequestModel) -> UserModel:
        if id != user_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to update user data with id:{id}"
            )
        user = await self.db.execute(select(UserModel).filter_by(id=id))
        user = user.scalar()

        if not user:
            raise NotFoundError(
                detail=f"User with id:{id} was not found!"
            )

        if user_data.password:
            hashed_password = HashPasswordHelper.create_hash_password(user_data.password)
            user_data.password = hashed_password

        for field, value in user_data:
            if value != None:
                setattr(user, field, value)

        user.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(user)
        logger.info(f"User with id:{id} updated successfully! 'data': {user_data.dict(exclude_unset=True)}")
        return user

    """Delete user by id"""
    async def delete_user(self, id: int, user_id: int):
        if id != user_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to delete user with id:{id}!"
            )
        await self._get_user_by_id(id=id)
        await self.db.execute(delete(UserModel).where(user_id == id))
        await self.db.commit()
        logger.info(f"User with id:{id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
