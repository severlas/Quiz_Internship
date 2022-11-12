from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditMixin(object):
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class BaseModel(Base, AuditMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, nullable=False)
