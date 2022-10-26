from fastapi import Depends, Response, status
from sqlalchemy import select, delete
from typing import List
from app.schemas.companies import CompanyAdmin
from app.schemas.users import NestedUser
from app.schemas.paginations import QuizPagination
from app.schemas.quiz import CreateQuiz, UpdateQuiz, Quiz, QuizDetail
from app.models.quiz import QuizModel, QuestionModel
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from log.config_log import logger
from datetime import datetime


class QuizService(BaseService):
    """Quiz CRUD"""

    """Protected method get quiz by id"""
    async def _get_quiz_by_id(self, id) -> QuizModel:
        quiz = await self.db.execute(select(QuizModel).filter_by(id=id))
        quiz = quiz.scalar()
        return quiz

    """Protected check permission"""
    async def _check_permission(self, company_id, user_id) -> PermissionError:
        admins = await self._get_admins_by_company_id(company_id)
        company = await self._get_company_by_id(company_id)
        if user_id != company.owner_id or user_id not in admins:
            raise PermissionError

    """Get list quiz"""
    async def get_list_quiz(self, id: int, user_id: int, pagination: QuizPagination) -> List[QuizModel]:
        members = await self._get_members_by_company_id(id)
        if user_id not in members:
            raise PermissionError
        quiz = await self.db.execute(
            select(QuizModel).
            limit(pagination.limit).offset(pagination.skip).
            filter_by(company_id=id)
        )
        quiz = quiz.scalars().all()
        return quiz

    """Get quiz by id"""
    async def get_quiz_by_id(self, id: int, quiz_id: int, user_id: int) -> QuizDetail:
        quiz = await self._get_quiz_by_id(id=quiz_id)

        if id != quiz.company_id:
            raise NotFoundError(
                detail=f"Quiz with id:{quiz_id} was not found in company!"
            )
        members = await self._get_members_by_company_id(id)
        if user_id not in members:
            raise PermissionError

        questions = await self.db.execute(select(QuestionModel).filter_by(quiz_id=quiz_id))
        questions = questions.scalars().all()

        quiz_data = QuizDetail(
            **quiz.__dict__,
            questions=questions
        )
        return quiz_data

    """Create quiz"""
    async def create_quiz(self, id: int, user_id: int, quiz_data: CreateQuiz) -> QuizModel:
        self._check_permission(company_id=id, user_id=user_id)

        quiz = QuizModel(
            **quiz_data.dict(),
            company_id=id,
            owner_id=user_id
        )
        self.db.add(quiz)
        await self.db.commit()
        await self.db.refresh(quiz)
        logger.info(f"Quiz created successfully! 'data': {quiz_data.dict()}")
        return quiz

    """Update quiz by id"""
    async def update_quiz(
            self,
            id: int,
            quiz_id: int,
            user_id: int,
            quiz_data: UpdateQuiz
    ) -> QuizModel:
        self._check_permission(company_id=id, user_id=user_id)
        quiz = self._get_quiz_by_id(id=quiz_id)

        for field, value in quiz_data:
            if value != None:
                setattr(quiz, field, value)

        await self.db.commit()
        await self.db.refresh(quiz)
        logger.info(
            f"Quiz with id:{quiz_id} updated successfully! "
            f"data': {quiz_data.dict(exclude_unset=True)}")
        return quiz

    """Delete quiz by id"""
    async def delete_quiz(self, id: int, quiz_id: int, user_id: int) -> Response:
        self._check_permission(company_id=id, user_id=user_id)

        await self.db.execute(delete(QuizModel).where(QuizModel.id == quiz_id))
        await self.db.commit()
        logger.info(f"Quiz with id:{quiz_id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
