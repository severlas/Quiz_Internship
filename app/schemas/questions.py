from pydantic import BaseModel, validator
from typing import List, Optional
from app.schemas.baseschemas import BaseMixin
from datetime import datetime


class BaseQuestion(BaseModel):
    name: str
    choice_answers: List[str]
    correct_answers: List[int]

    @validator('choice_answers')
    def check_number_of_choice_answers(cls, value):
        if len(value) < 2:
            raise ValueError('Question must be have min 2 choice answer')
        return value

    @validator('correct_answers')
    def check_number_of_correct_answers(cls, value, values, **kwargs):
        if len(value) == 0:
            raise ValueError('Question must be have min 1 correct answer')
        for v in value:
            if v >= len(values['choice_answers']):
                raise ValueError('Index out of range')
        return value


class CreateQuestion(BaseQuestion):
    pass


class UpdateQuestion(BaseQuestion):
    name: Optional[str] = None
    choice_answers: Optional[List[str]] = None
    correct_answers: Optional[List[int]] = None


class NestedQuestion(BaseQuestion):
    id: int

    class Config:
        orm_mode = True


class Question(NestedQuestion):
    quiz_id: int

