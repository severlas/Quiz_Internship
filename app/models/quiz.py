from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey, Enum
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship
from app.models.basemodel import BaseModel
from app.models.companies import *
from app.models.users import *


class QuizModel(BaseModel):
    __tablename__ = 'quiz'

    name = Column(String(100), nullable=False)
    descriptions = Column(String(1000), nullable=True)
    frequency = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))

    owner = relationship('UserModel', back_populates='quiz')
    questions = relationship('QuestionModel', back_populates='quiz')
    company = relationship('CompanyModel', back_populates='quiz')


class QuestionModel(BaseModel):
    __tablename__ = 'questions'

    name = Column(String(1000), nullable=False)
    choice_answers = Column(ARRAY(String))
    correct_answer = Column(Integer, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'))

    quiz = relationship('QuizModel', back_populates="questions")


# class QuizResult(BaseModel):
#     pass
