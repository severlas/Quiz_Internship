from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm


class BaseUser(BaseModel):
    email: EmailStr


class SignUpRequestModel(BaseUser):
    username: str
    password: str


class SignInRequestModel(OAuth2PasswordRequestForm):
    pass


class UserUpdateRequestModel(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None
    is_admin: Union[bool, None] = False
    is_staff: Union[bool, None] = False
    is_active: Union[bool, None] = True


class User(BaseUser):
    id: int
    username: str
    is_admin: bool = False
    is_staff: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        

class UserPagination(BaseModel):
    limit: int = 5
    skip: int = 0


class UserJWT(BaseUser):
    id: int

    class Config:
        orm_mode = True


class TokenJWT(BaseModel):
    access_token: str
    token_type: str = 'bearer'
