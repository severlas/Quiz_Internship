from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from app.services.requests_utils import RequestStatus, RequestSender
from app.schemas.baseschemas import BaseMixin


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


class Request(BaseRequest, BaseMixin):
    id: int
    company_id: int
    user_id: int

    class Config:
        orm_mode = True


class RequestDetail(Request):
    pass
