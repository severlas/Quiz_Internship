from pydantic import BaseModel
from typing import List, Optional
from app.schemas.baseschemas import BaseMixin
from datetime import datetime


class BaseQuestion(BaseModel):
    name: str
    choice_answers: List[str]
    correct_answer: int


class CreateQuestion(BaseQuestion):
    pass


class UpdateQuestion(BaseModel):
    name: Optional[str] = None
    choice_answers: Optional[List[str]] = None
    correct_answer: Optional[int] = None
    updated_at: datetime = datetime.now()


class NestedQuestion(BaseQuestion):
    id: int

    class Config:
        orm_mode = True


class Question(BaseQuestion):
    id: int
    quiz_id: int
    correct_answer: int

    class Config:
        orm_mode = True


# class QuestionDetail()
