from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey, Enum
from sqlalchemy.dialects import postgresql
from app.basemodel import BaseModel
from sqlalchemy.orm import declarative_base, relationship
from app.services.requests_utils import RequestStatus, RequestSender

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


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150))
    is_active = Column(Boolean, server_default='True', nullable=False)
    company = relationship('Company', back_populates='owner')

    companies_admins = relationship(
        "Company", secondary=admins, back_populates="admins"
    )
    companies_members = relationship(
        "Company", secondary=members, back_populates="members"
    )


class Company(BaseModel):
    __tablename__ = 'companies'

    name = Column(String(100), unique=True, nullable=False)
    descriptions = Column(String(1000))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    visibility = Column(Boolean, server_default='True')

    owner = relationship('User', back_populates="company")
    admins = relationship(
        "User", secondary=admins, back_populates="companies_admins"
    )
    members = relationship(
        "User", secondary=members, back_populates="companies_members"
    )


class Request(BaseModel):

    __tablename__ = 'requests'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    status = Column(postgresql.ENUM(RequestStatus), default=RequestStatus.CREATED, nullable=True)
    sender = Column(postgresql.ENUM(RequestSender), default=RequestSender.USER, nullable=True)
