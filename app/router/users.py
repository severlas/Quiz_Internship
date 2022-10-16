from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.users import User, UserUpdateRequestModel, SignUpRequestModel, UserPagination
from app.services.users import UserService

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get('/', response_model=List[User])
def get_users(pagination: UserPagination = Depends(), service: UserService = Depends()):
    return service.get_users(pagination)


@router.get('/{id}', response_model=User)
def get_user(id: int, service: UserService = Depends()):
    return service.get_user(user_id=id)


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
        user_data: SignUpRequestModel,
        service: UserService = Depends()
):
    return service.create_user(user_data=user_data)


@router.put('/{id}', response_model=User)
def update_user(
        id: int,
        user_data: UserUpdateRequestModel,
        service: UserService = Depends()
):
    return service.update_user(user_id=id, user_data=user_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, service: UserService = Depends()):
    return service.delete_user(user_id=id)
