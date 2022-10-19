from sqlalchemy import Column, String, Integer, Boolean
from app.basemodel import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150))
    is_admin = Column(Boolean, server_default='False', nullable=False)
    is_staff = Column(Boolean, server_default='False', nullable=False)
    is_active = Column(Boolean, server_default='True', nullable=False)

