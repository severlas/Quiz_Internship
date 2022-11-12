from pydantic import BaseModel
from typing import List


class BaseUpload(BaseModel):
    quiz_id: int
    question: str
    answers: str


class UploadQuizAnswersForCompany(BaseUpload):
    user_id: int


class UploadQuizAnswersForUser(BaseUpload):
    company_id: int

