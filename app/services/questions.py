from fastapi import Depends, Response, status
from sqlalchemy import select, delete
from typing import List
from app.schemas.companies import CompanyAdmin
from app.schemas.users import NestedUser
from app.schemas.paginations import QuizPagination
from app.schemas.questions import CreateQuestion, UpdateQuestion, Question
from app.models.quiz import QuestionModel, QuizModel
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from log.config_log import logger
from datetime import datetime


class QuestionService(BaseService):
    """Question CRUD"""

    """Protected method get question by id"""
    async def _get_question_by_id(self, id) -> QuestionModel:
        question = await self.db.execute(select(QuestionModel).filter_by(id=id))
        question = question.scalar()
        return question

    """Check permission"""
    async def _check_permission(self, company_id: int, user_id: int, quiz_id: int):
        quiz = await self.db.execute(select(QuizModel).filter_by(id=quiz_id))
        quiz = quiz.scalar()

        if company_id != quiz.company_id:
            raise NotFoundError(
                detail=f"Quiz with id:{quiz_id} was not found in company with id:{company_id}"
            )
        if user_id != quiz.owner_id:
            raise PermissionError

    """Get list questions"""
    async def get_questions(
            self,
            company_id: int,
            quiz_id: int,
            user_id: int,
            pagination: QuizPagination
    ) -> List[QuestionModel]:
        members = await self._get_members_by_company_id(id=company_id)
        if user_id not in members:
            raise PermissionError
        questions = await self.db.execute(
            select(QuestionModel).
            limit(pagination.limit).offset(pagination.skip).
            filter_by(quiz_id=quiz_id)
        )
        questions = questions.scalars().all()
        return questions

    """Create question"""
    async def create_question(
            self,
            company_id: int,
            quiz_id: int,
            user_id: int,
            question_data: CreateQuestion
    ) -> QuestionModel:
        self._check_permission(company_id=company_id, user_id=user_id, quiz_id=quiz_id)
        question = QuestionModel(**question_data.dict(), quiz_id=quiz_id)

        self.db.add(question)
        await self.db.commit()
        await self.db.refresh(question)
        logger.info(f"Question created successfully! data': {question_data.dict()}")
        return question

    """Update question by id"""
    async def update_question(
            self,
            company_id: int,
            quiz_id: int,
            user_id: int,
            question_id: int,
            question_data: UpdateQuestion
    ) -> QuestionModel:
        self._check_permission(company_id=company_id, user_id=user_id, quiz_id=quiz_id)
        question = self._get_question_by_id(id=question_id)
        for field, value in question_data:
            if value != None:
                setattr(question, field, value)

        await self.db.commit()
        await self.db.refresh(question)
        logger.info(
            f"Question with id:{question_id} updated successfully! "
            f"'data': {question_data.dict(exclude_unset=True)}"
        )
        return question

    """Delete question by id"""
    async def delete_question(
            self,
            company_id: int,
            quiz_id: int,
            user_id: int,
            question_id: int,
    ) -> Response:
        self._check_permission(company_id=company_id, user_id=user_id, quiz_id=quiz_id)

        await self.db.execute(delete(QuestionModel).where(QuestionModel.id == question_id))
        await self.db.commit()
        logger.info(f"Question with id:{question_id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)





