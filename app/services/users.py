from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_postgres_db
from app import models
from app.schemas.users import User
from passlib.context import CryptContext


class UserService:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def __init__(self, db: Session = Depends(get_postgres_db)):
        self.db = db

    @classmethod
    def create_hash_password(cls, password: int) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    def get_users(self) -> List[User]:
        users = self.db.query(models.User).all()
        return users
