from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AnalyticsGPA(BaseModel):
    gpa_all: float

    class Config:
        orm_mode = True


class GPAByQuiz(BaseModel):
    gpa_by_quiz: float
    created_at: datetime

    class Config:
        orm_mode = True


class AnalyticsGPAByQuiz(BaseModel):
    quiz_id: int
    gpa_over_time: List[GPAByQuiz]

    class Config:
        orm_mode = True


class GPAOverTime(BaseModel):
    gpa_all: float
    created_at: datetime

    class Config:
        orm_mode = True


class AnalyticsGPAForCompany(BaseModel):
    user_id: int
    gpa_over_time: List[GPAOverTime]

    class Config:
        orm_mode = True


class TimeOfLastQuiz(BaseModel):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TimeOfLastQuizForUser(BaseModel):
    quiz_id: int
    created_at: datetime

    class Config:
        orm_mode = True
