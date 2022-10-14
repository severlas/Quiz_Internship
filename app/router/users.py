from fastapi import APIRouter, Depends
from typing import List
from app.schemas.users import User
from app.services.users import UserService

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get('/', response_model=List[User])
def get_users(service: UserService = Depends()):
    return service.get_users()
