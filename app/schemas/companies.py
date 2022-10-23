from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union, List
from fastapi.param_functions import Form
from app import models
from app.schemas.requests import Request, NestedRequestInCompany
from app.schemas.users import NestedUser


class BaseCompany(BaseModel):
    name: str
    descriptions: str
    visibility: bool = True


class CreateCompany(BaseCompany):
    pass


class UpdateCompany(BaseCompany):
    pass


class Company(BaseCompany):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class NestedCompany(BaseCompany):
    id: int

    class Config:
        orm_mode = True


class CompanyDetail(Company):
    admins: List[dict] = []
    staff: List[dict] = []
    requests: List[NestedRequestInCompany] = []

    class Config:
        orm_mode = True


class CompanyAdmin(BaseModel):
    company_id: int
    admin: NestedUser

    class Config:
        orm_mode = True
