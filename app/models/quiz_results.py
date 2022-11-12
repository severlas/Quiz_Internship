from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship
from app.models.basemodel import BaseModel


class QuizResultModel(BaseModel):
    __tablename__ = "quiz_results"

    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    number_of_questions = Column(Integer, nullable=False)
    number_of_correct_answers = Column(Integer, nullable=False)
    sum_questions_by_quiz = Column(Integer, nullable=False)
    sum_correct_answers_by_quiz = Column(Integer, nullable=False)
    sum_all_questions = Column(Integer, nullable=False)
    sum_all_correct_answers = Column(Integer, nullable=False)
    gpa = Column(Float, nullable=False)
    gpa_by_quiz = Column(Float, nullable=False)
    gpa_all = Column(Float, nullable=False)

    user = relationship('UserModel', back_populates="quiz_results")
    quiz = relationship('QuizModel', back_populates="quiz_results")
    company = relationship('CompanyModel', back_populates="quiz_results")


