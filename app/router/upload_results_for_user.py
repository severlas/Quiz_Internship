from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from typing import List, Optional
from app.services.upload_results import UploadResultService
from app.schemas.upload_results import UploadQuizAnswersForUser
from app.schemas.quiz import QuizResult
from app.models.users import UserModel
from app.models.quiz_results import QuizResultModel
from app.services.auth import get_current_user


router = APIRouter(
    prefix='/{id}',
    tags=['Upload']
)


@router.get('/upload_results', response_model=List[QuizResult])
async def get_upload_results(
        id: int,
        company_id: Optional[int] = None,
        quiz_id: Optional[int] = None,
        user: UserModel = Depends(get_current_user),
        service: UploadResultService = Depends()
) -> List[QuizResult]:
    return await service.get_quiz_results_for_user(id=id, user_id=user.id, company_id=company_id, quiz_id=quiz_id)


@router.get('/export_results')
async def get_export_results_to_csv(
        id: int,
        company_id: Optional[int] = None,
        quiz_id: Optional[int] = None,
        filename: Optional[str] = "export",
        user: UserModel = Depends(get_current_user),
        service: UploadResultService = Depends()
) -> StreamingResponse:
    return await service.export_results_for_user(
        id=id,
        user_id=user.id,
        company_id=company_id,
        quiz_id=quiz_id,
        filename=filename
    )


@router.get('/upload_answers', response_model=List[UploadQuizAnswersForUser])
async def get_upload_answers(
        id: int,
        company_id: Optional[int] = None,
        quiz_id: Optional[int] = None,
        user: UserModel = Depends(get_current_user),
        service: UploadResultService = Depends()
) -> List[UploadQuizAnswersForUser]:
    return await service.get_quiz_answers_for_user(id=id, user_id=user.id, company_id=company_id, quiz_id=quiz_id)


@router.get('/export_answers')
async def get_export_answers_to_csv(
        id: int,
        company_id: Optional[int] = None,
        quiz_id: Optional[int] = None,
        filename: Optional[str] = "export",
        user: UserModel = Depends(get_current_user),
        service: UploadResultService = Depends()
) -> StreamingResponse:
    return await service.export_answers_for_user(
        id=id,
        user_id=user.id,
        company_id=company_id,
        quiz_id=quiz_id,
        filename=filename
    )

