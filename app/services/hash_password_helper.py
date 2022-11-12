from passlib.context import CryptContext


class HashPasswordHelper:
    """Create and verify password"""

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    """Create hash password"""
    @classmethod
    def create_hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    """Verify password"""
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)
