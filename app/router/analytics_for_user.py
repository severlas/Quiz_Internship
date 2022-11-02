from fastapi import APIRouter, Depends
from typing import Optional, List
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsGPAByQuiz, AnalyticsGPA, TimeOfLastQuizForUser
from app.models.users import UserModel
from app.models.quiz_results import QuizResultModel
from app.services.auth import get_current_user

router = APIRouter(
    prefix='/{id}',
    tags=['Analytics']
)


@router.get('/get_gpa', response_model=AnalyticsGPA)
async def get_gpa_all(id: int, service: AnalyticsService = Depends()) -> QuizResultModel:
    return await service.get_gpa_for_user(id=id)


@router.get('/get_gpa_by_quiz', response_model=List[AnalyticsGPAByQuiz])
async def get_gpa_by_quiz(
        id: int,
        user: UserModel = Depends(get_current_user),
        service: AnalyticsService = Depends()
) -> List[AnalyticsGPAByQuiz]:
    return await service.get_gpa_by_quiz_for_user(id=id, user_id=user.id)


@router.get('/get_time_of_last_quiz', response_model=List[TimeOfLastQuizForUser])
async def get_time_of_last_quiz(
        id: int,
        user: UserModel = Depends(get_current_user),
        service: AnalyticsService = Depends()
) -> List[QuizResultModel]:
    return await service.get_quizzes_and_time_of_last_quiz(id=id, user_id=user.id)
