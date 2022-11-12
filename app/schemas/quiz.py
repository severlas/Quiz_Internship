from pydantic import BaseModel, validator
from typing import List, Optional
from app.schemas.baseschemas import BaseMixin
from app.schemas.questions import NestedQuestion
from datetime import datetime


class BaseQuiz(BaseModel):
    name: str
    descriptions: Optional[str] = None
    frequency: int

    @validator('frequency')
    def check_frequency(cls, value):
        if value <= 0:
            raise ValueError('Frequency must be more than 0')
        return value


class CreateQuiz(BaseQuiz):
    pass


class UpdateQuiz(BaseModel):
    name: Optional[str] = None
    descriptions: Optional[str] = None
    frequency: Optional[int] = None
    update_at: datetime = datetime.now()

    @validator('frequency')
    def check_frequency(cls, value):
        if value <= 0:
            raise ValueError('Frequency must be more than 0')
        return value


class Quiz(BaseQuiz, BaseMixin):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class QuizDetail(Quiz):
    questions: List[NestedQuestion]

    @validator('questions')
    def check_questions_quantity(cls, value):
        if len(value) < 2:
            raise ValueError('Questions quantity must be more than 2')
        return value


class TakeQuiz(BaseModel):
    question_id: int
    answers: List[int]


class QuizResult(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    company_id: int
    number_of_questions: int
    number_of_correct_answers: int
    sum_all_questions: int
    sum_all_correct_answers: int
    gpa: float
    gpa_all: float
    created_at: datetime

    class Config:
        orm_mode = True
