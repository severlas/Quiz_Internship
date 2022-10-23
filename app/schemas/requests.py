from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class RequestStatus(str, Enum):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'


class RequestSender(str, Enum):
    USER = 'user'
    COMPANY = 'company'


class BaseRequest(BaseModel):
    sender: RequestSender
    status: RequestStatus


class NestedRequestInCompany(BaseRequest):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class NestedRequestInUser(BaseRequest):
    id: int
    company_id: int

    class Config:
        orm_mode = True


class CreateRequest(BaseRequest):
    company_id: int
    user_id: int


class Request(BaseRequest):
    id: int
    company_id: int
    user_id: int
    # user: OutUser
    # company: Company
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RequestDetail(Request):
    pass
