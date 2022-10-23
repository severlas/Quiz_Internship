from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union, List
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.requests import NestedRequestInUser


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class SignUpRequestModel(BaseUser):
    password: str


class SignInRequestModel(OAuth2PasswordRequestForm):
    pass


class UserUpdateRequestModel(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None
    is_active: Union[bool, None] = True


class NestedUser(BaseUser):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class User(NestedUser):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserDetail(User):
    requests: List[NestedRequestInUser] = []


class UserJWT(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class TokenJWT(BaseModel):
    access_token: str
    token_type: str = 'bearer'
