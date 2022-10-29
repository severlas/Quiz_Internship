from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey
from app.models.basemodel import BaseModel
from sqlalchemy.orm import relationship
from app.models.quiz import *
from app.models.companies import *


class UserModel(BaseModel):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150))
    is_active = Column(Boolean, server_default='True', nullable=False)
    company = relationship('CompanyModel', back_populates='owner')
    quiz = relationship('QuizModel', back_populates='owner')

    companies_admins = relationship(
        "CompanyModel", secondary=admins, back_populates="admins"
    )
    companies_members = relationship(
        "CompanyModel", secondary=members, back_populates="members"
    )