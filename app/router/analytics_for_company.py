from fastapi import APIRouter, Depends
from typing import Optional, List
from app.services.analytics import AnalyticsService
from app.schemas.analytics import AnalyticsGPAByQuiz, AnalyticsGPA, AnalyticsGPAForCompany, TimeOfLastQuiz
from app.models.users import UserModel
from app.models.quiz_results import QuizResultModel
from app.services.auth import get_current_user

router = APIRouter(
    prefix='/{company_id}',
    tags=['Analytics']
)


@router.get('/get_gpa', response_model=List[AnalyticsGPAForCompany])
async def get_gpa_all_user(
        company_id: int,
        user: UserModel = Depends(get_current_user),
        service: AnalyticsService = Depends()
) -> List[AnalyticsGPAForCompany]:
    return await service.get_gpa_for_company(company_id=company_id, user_id=user.id)


@router.get('/get_gpa_by_quiz', response_model=List[AnalyticsGPAByQuiz])
async def get_gpa_by_quiz(
        company_id: int,
        quiz_user_id: int,
        user: UserModel = Depends(get_current_user),
        service: AnalyticsService = Depends()
) -> List[AnalyticsGPAByQuiz]:
    return await service.get_gpa_by_quiz(company_id=company_id, user_id=user.id, quiz_user_id=quiz_user_id)


@router.get('/get_time_of_last_quiz', response_model=List[TimeOfLastQuiz])
async def get_time_of_last_quiz(
        company_id: int,
        user: UserModel = Depends(get_current_user),
        service: AnalyticsService = Depends()
) -> List[QuizResultModel]:
    return await service.get_users_and_time_of_last_quiz(company_id=company_id, user_id=user.id)
