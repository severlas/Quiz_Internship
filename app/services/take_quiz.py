from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.sql import func
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.quiz import CreateQuiz, UpdateQuiz, Quiz, QuizDetail, TakeQuiz
from app.models.quiz import QuizModel, QuestionModel
from app.models.quiz_results import QuizResultModel
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from log.config_log import logger
from datetime import datetime
from app.settings import settings
from app.database import get_redis_db, get_postgres_db
from aioredis import Redis
import json


class TakeQuizService(BaseService):
    """Take to quiz"""
    EXPIRE_RESULTS = 60 * 60 * 48

    def __init__(self, db_redis: Redis = Depends(get_redis_db), db: AsyncSession = Depends(get_postgres_db)):
        self.db_redis = db_redis
        self.db = db

    """Protected method get quiz result by user id"""
    async def _get_quiz_results_by_user_id(self, user_id: int) -> List[QuizResultModel]:
        quiz_results = await self.db.execute(select(QuizResultModel).filter_by(user_id=user_id))
        quiz_results = quiz_results.scalars().all()
        return quiz_results

    """Protected method get questions by quiz id"""
    async def _get_questions_by_quiz_id(self, quiz_id: int) -> List[QuestionModel]:
        questions = await self.db.execute(select(QuestionModel).filter_by(quiz_id=quiz_id))
        questions = questions.scalars().all()
        return questions

    async def take_quiz(
            self,
            company_id: int,
            quiz_id: int,
            user_id: int,
            quiz_data: List[TakeQuiz]
    ) -> QuizResultModel:
        questions = await self._get_questions_by_quiz_id(quiz_id=quiz_id)
        if len(questions) < 2:
            raise NotFoundError(
                detail=f"Quiz with id:{quiz_id} was not found!"
            )
        members = await self._get_members_by_company_id(company_id)
        if user_id not in members:
            raise PermissionError(
                log_detail=f"User with id:{user_id} isn't member company with id:{company_id}"
            )
        data = {question.question_id: question.answers for question in quiz_data}

        redis_data = {
            question.name: [question.choice_answers[el]
                            for el in data.get(question.id)]
            for question in questions
        }

        await self.db_redis.set(
            f'user_id:{user_id}_company_id:{company_id}_quiz_id:{quiz_id}',
            json.dumps(redis_data),
            ex=self.EXPIRE_RESULTS
        )

        number_of_questions = len(questions)
        number_of_correct_answers = len([
            question for question in questions
            if question.correct_answers == data.get(question.id)
        ])
        quiz_results = await self._get_quiz_results_by_user_id(user_id=user_id)

        if quiz_results:
            sum_all_questions = quiz_results[-1].sum_all_questions + number_of_questions
            sum_all_correct_answers = quiz_results[-1].sum_all_correct_answers + number_of_correct_answers
        else:
            sum_all_questions = number_of_questions
            sum_all_correct_answers = number_of_correct_answers

        quiz_result = QuizResultModel(
            quiz_id=quiz_id,
            user_id=user_id,
            company_id=company_id,
            number_of_questions=number_of_questions,
            number_of_correct_answers=number_of_correct_answers,
            sum_all_questions=sum_all_questions,
            sum_all_correct_answers=sum_all_correct_answers,
            gpa=round(number_of_correct_answers / number_of_questions, 3),
            gpa_all=round(sum_all_correct_answers / sum_all_questions, 3)
        )

        self.db.add(quiz_result)
        await self.db.commit()
        await self.db.refresh(quiz_result)
        logger.info(f"User with id:{user_id} take to quiz with id:{quiz_id}!")
        return quiz_result
