from pydantic import BaseModel, EmailStr
from datetime import datetime


class BaseUser(BaseModel):
    email: EmailStr


class SignUpRequestModel(BaseUser):
    username: str
    password: str


class SignInRequestModel(BaseUser):
    password: str


class UserUpdateRequestModel(BaseUser):
    username: str
    is_admin: bool = False
    is_staff: bool = False
    is_active: bool = True


class User(UserUpdateRequestModel):
    id: int
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
