from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects import postgresql
from app.models.basemodel import BaseModel
from app.services.requests_utils import RequestStatus, RequestSender


class RequestModel(BaseModel):

    __tablename__ = 'requests'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    status = Column(postgresql.ENUM(RequestStatus), default=RequestStatus.CREATED, nullable=True)
    sender = Column(postgresql.ENUM(RequestSender), default=RequestSender.USER, nullable=True)
