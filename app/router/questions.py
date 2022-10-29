from fastapi import APIRouter, Depends, status, Response
from typing import List
from app.services.questions import QuestionService
from app.schemas.questions import CreateQuestion, UpdateQuestion, Question
from app.schemas.companies import NestedUser
from app.schemas.paginations import QuizPagination
from app.services.auth import get_current_user
from app.models.users import UserModel
from app.models.quiz import QuestionModel


router = APIRouter(
    prefix='/{quiz_id}/questions',
)


@router.get('/')
async def get_questions(
        id: int,
        quiz_id: int,
        pagination: QuizPagination = Depends(),
        service: QuestionService = Depends(),
        user: UserModel = Depends(get_current_user),
) -> List[QuestionModel]:
    return await service.get_questions(id=id, quiz_id=quiz_id, user_id=user.id, pagination=pagination)


@router.post('/', response_model=Question, status_code=status.HTTP_201_CREATED)
async def create_question(
        id: int,
        quiz_id: int,
        question_data: CreateQuestion,
        user: UserModel = Depends(get_current_user),
        service: QuestionService = Depends()
) -> QuestionModel:
    return await service.create_question(
        id=id,
        quiz_id=quiz_id,
        question_data=question_data,
        user_id=user.id
    )


@router.put('/{question_id}', response_model=Question)
async def update_question(
        id: int,
        quiz_id: int,
        question_id: int,
        question_data: UpdateQuestion,
        user: UserModel = Depends(get_current_user),
        service: QuestionService = Depends()
) -> QuestionModel:
    return await service.update_question(
        id=id,
        quiz_id=quiz_id,
        question_id=question_id,
        question_data=question_data,
        user_id=user.id
    )


@router.delete('/{question_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
        id: int,
        quiz_id: int,
        question_id: int,
        user: UserModel = Depends(get_current_user),
        service: QuestionService = Depends()
) -> Response:
    return await service.delete_question(
        id=id,
        quiz_id=quiz_id,
        user_id=user.id,
        question_id=question_id
    )
