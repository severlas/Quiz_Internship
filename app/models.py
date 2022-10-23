from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey
from app.basemodel import BaseModel
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy_utils.types.choise import ChoiseType
from sqlalchemy_utils.types import choice
# from babel import lazy_gettext as _

admins = Table(
    "admins",
    BaseModel.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('company_id', ForeignKey('companies.id'), primary_key=True)
)


staff = Table(
    "staff",
    BaseModel.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('company_id', ForeignKey('companies.id'), primary_key=True)
)


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150))
    is_active = Column(Boolean, server_default='True', nullable=False)
    company = relationship('Company')

    companies_admin = relationship(
        "Company", secondary=admins, back_populates="admins"
    )
    companies_staff = relationship(
        "Company", secondary=staff, back_populates="staff"
    )


class Company(BaseModel):
    __tablename__ = 'companies'

    name = Column(String(100), unique=True, nullable=False)
    descriptions = Column(String(1000))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    visibility = Column(Boolean, server_default='True')

    owner = relationship('User')
    admins = relationship(
        "User", secondary=admins, back_populates="companies_admin"
    )
    staff = relationship(
        "User", secondary=staff, back_populates="companies_staff"
    )


class Request(BaseModel):

    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    CREATED = 'created'

    REQUEST_STATUS = [
        (CONFIRMED, 'confirmed'),
        (REJECTED, 'canceled'),
        (CREATED, 'completed')
    ]

    USER = 'user'
    COMPANY = 'company'

    REQUEST_SENDER = [
        (USER, 'user'),
        (COMPANY, 'company')
    ]

    __tablename__ = 'requests'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    status = Column(choice.ChoiceType(REQUEST_STATUS), server_default=CREATED, nullable=False)
    sender = Column(choice.ChoiceType(REQUEST_SENDER), server_default=USER, nullable=False)
