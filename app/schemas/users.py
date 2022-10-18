from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime


class BaseUser(BaseModel):
    email: EmailStr


class SignUnRequestModel(BaseUser):
    username: str
    password: str


class SignUpRequestModel(BaseUser):
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
