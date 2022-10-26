from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey, Enum
from sqlalchemy.dialects import postgresql
from app.models.basemodel import BaseModel
from sqlalchemy.orm import declarative_base, relationship
from app.services.requests_utils import RequestStatus, RequestSender
from app.models.quiz import *
from app.models.users import *

admins = Table(
    "admins",
    BaseModel.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('company_id', ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True)
)


members = Table(
    "members",
    BaseModel.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('company_id', ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True)
)


class CompanyModel(BaseModel):
    __tablename__ = 'companies'

    name = Column(String(100), unique=True, nullable=False)
    descriptions = Column(String(1000))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    visibility = Column(Boolean, server_default='True')

    owner = relationship('UserModel', back_populates="company")
    quiz = relationship('QuizModel', back_populates='company')
    admins = relationship(
        "UserModel", secondary=admins, back_populates="companies_admins"
    )
    members = relationship(
        "UserModel", secondary=members, back_populates="companies_members"
    )