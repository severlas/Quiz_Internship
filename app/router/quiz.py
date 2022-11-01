from fastapi import APIRouter, Depends, status, Response
from typing import List
from app.services.quiz import QuizService
from app.schemas.quiz import CreateQuiz, UpdateQuiz, Quiz, QuizDetail, TakeQuiz, QuizResult
from app.services.take_quiz import TakeQuizService
from app.schemas.companies import NestedUser
from app.schemas.paginations import QuizPagination
from app.services.auth import get_current_user
from app.models.users import UserModel
from app.models.quiz import QuizModel
from app.models.quiz_results import QuizResultModel
from app.router.questions import router as questions_router


router = APIRouter(
    prefix='/{company_id}/quiz'
)


@router.get('/', response_model=List[Quiz])
async def get_list_quiz(
        company_id: int,
        pagination: QuizPagination = Depends(),
        service: QuizService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> List[QuizModel]:
    return await service.get_list_quiz(company_id=company_id, user_id=user.id, pagination=pagination)


@router.get('/{quiz_id}', response_model=QuizDetail)
async def get_quiz_by_id(
        company_id: int,
        quiz_id: int,
        service: QuizService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> QuizDetail:
    return await service.get_quiz_by_id(company_id=company_id, quiz_id=quiz_id, user_id=user.id)


@router.post('/', response_model=Quiz, status_code=status.HTTP_201_CREATED)
async def create_quiz(
        company_id: int,
        quiz_data: CreateQuiz,
        service: QuizService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> QuizModel:
    return await service.create_quiz(company_id=company_id, quiz_data=quiz_data, user_id=user.id)


@router.put('/{quiz_id}', response_model=Quiz)
async def update_quiz(
        company_id: int,
        quiz_id: int,
        quiz_data: UpdateQuiz,
        service: QuizService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> QuizModel:
    return await service.update_quiz(
        company_id=company_id,
        quiz_id=quiz_id,
        quiz_data=quiz_data,
        user_id=user.id
    )


@router.delete('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
        company_id: int,
        quiz_id: int,
        service: QuizService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> Response:
    return await service.delete_quiz(company_id=company_id, quiz_id=quiz_id, user_id=user.id)


router.include_router(questions_router)


@router.post('/{quiz_id}/take_quiz', response_model=QuizResult, status_code=status.HTTP_201_CREATED)
async def take_quiz(
        company_id: int,
        quiz_id: int,
        quiz_data: List[TakeQuiz],
        user: UserModel = Depends(get_current_user),
        service: TakeQuizService = Depends()
) -> QuizResultModel:
    return await service.take_quiz(
        company_id=company_id,
        quiz_id=quiz_id,
        quiz_data=quiz_data,
        user_id=user.id
    )
