from fastapi import APIRouter, Depends, status, Response
from typing import List, Optional, Union
from app.schemas.users import User, UserUpdateRequestModel, SignUpRequestModel, UserDetail
from app.schemas.paginations import UserPagination
from app.services.users import UserService
from app.services.auth import get_current_user
from app.models.users import UserModel

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get('/', response_model=List[User])
async def get_users(
        pagination: UserPagination = Depends(),
        service: UserService = Depends(),
) -> List[UserModel]:
    return await service.get_users(pagination=pagination)


@router.get('/{id}', response_model=UserDetail)
async def get_user(
        id: int,
        service: UserService = Depends(),
) -> UserDetail:
    return await service.get_user(id=id)


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: SignUpRequestModel,
        service: UserService = Depends()
) -> UserModel:
    return await service.create_user(user_data=user_data)


@router.put('/{id}', response_model=User)
async def update_user(
        id: int,
        user_data: UserUpdateRequestModel,
        service: UserService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> UserModel:
    return await service.update_user(id=id, user_data=user_data, user_id=user.id)


@router.patch('/{id}', response_model=User)
async def update_field_user(
        id: int,
        user_data: UserUpdateRequestModel,
        service: UserService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> UserModel:
    return await service.update_user(id=id, user_data=user_data, user_id=user.id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        id: int, service: UserService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> Response:
    return await service.delete_user(id=id, user_id=user.id)
