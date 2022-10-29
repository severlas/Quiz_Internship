from pydantic import BaseModel
from typing import List, Optional
from app.schemas.baseschemas import BaseMixin
from app.schemas.questions import NestedQuestion
from datetime import datetime


class BaseQuiz(BaseModel):
    name: str
    descriptions: Optional[str] = None
    frequency: int


class CreateQuiz(BaseQuiz):
    pass


class UpdateQuiz(BaseModel):
    name: Optional[str] = None
    descriptions: Optional[str] = None
    frequency: Optional[int] = None
    update_at: datetime = datetime.now()


class Quiz(BaseQuiz, BaseMixin):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class QuizDetail(Quiz):
    questions: List[NestedQuestion]
