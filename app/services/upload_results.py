from fastapi import Depends
from fastapi.responses import StreamingResponse
from typing import Optional, List
from sqlalchemy import select
from app.services.baseservice import BaseService
from app.services.exceptions import NotFoundError, PermissionError
from aioredis import Redis
from io import StringIO
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.upload_results import UploadQuizAnswersForCompany, UploadQuizAnswersForUser
from app.schemas.quiz import QuizResult
from app.models.quiz_results import QuizResultModel
from app.database import get_redis_db, get_postgres_db
from aioredis import Redis
import csv
import json


class UploadResultService(BaseService):
    def __init__(self, db_redis: Redis = Depends(get_redis_db), db: AsyncSession = Depends(get_postgres_db)):
        self.db_redis = db_redis
        self.db = db

    @staticmethod
    def find_index(key: str, value: str) -> int:
        return key.index(value) + len(value) + 1

    @staticmethod
    def _export_to_csv(values: list, filename: str) -> StreamingResponse:
        export = StringIO()
        writer = csv.DictWriter(
            export,
            fieldnames=list(values[0].dict().keys()),
            extrasaction='ignore'
        )
        writer.writeheader()
        for value in values:
            writer.writerow(value.dict())
        export.seek(0)

        return StreamingResponse(
            export,
            media_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

    async def _check_permission_for_company(self, company_id: int, user_id: int) -> PermissionError:
        admins = await self._get_admins_by_company_id(company_id)

        if user_id not in admins:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to get information about company with id:{company_id}!"
            )

    async def _get_quiz_answers_for_user(
            self,
            id: int,
            user_id: int,
            company_id: Optional[int] = None,
            quiz_id: Optional[int] = None
    ) -> List[UploadQuizAnswersForUser]:
        if user_id != id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to see information about user with id:{id}!"
            )
        find_keys = f'user_id:{user_id}'
        if company_id:
            find_keys = find_keys + f'_company_id:{company_id}'
            if quiz_id:
                find_keys = find_keys + f'_quiz_id:{quiz_id}'
        keys = await self.db_redis.keys(f'*{find_keys}*')
        answers = []
        for key in keys:
            questions = json.loads(await self.db_redis.get(key))
            for question in questions:
                answers.append(
                    ExportQuizForUser(
                        company_id=key[self.find_index(key, 'company_id'): self.find_index(key, 'company_id') + 1],
                        quiz_id=key[self.find_index(key, 'quiz_id'):],
                        question=question,
                        answers=', '.join(questions.get(question))
                    )
                )

        return answers

    async def _get_quiz_results_for_user(
            self,
            id: int,
            user_id: int,
            company_id: Optional[int] = None,
            quiz_id: Optional[int] = None
    ) -> List[QuizResult]:
        if user_id != id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to get information about user with id:{id}!"
            )
        query = select(QuizResultModel).filter_by(user_id=user_id)
        if company_id:
            query = query.filter_by(company_id=company_id)
        if quiz_id:
            query = query.filter_by(quiz_id=quiz_id)
        quiz_results = await self.db.execute(query)
        quiz_results = quiz_results.scalars().all()
        return [QuizResult.from_orm(quiz_result) for quiz_result in quiz_results]

    async def _get_quiz_results_for_company(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: Optional[int] = None,
            quiz_id: Optional[int] = None
    ) -> List[QuizResult]:
        await self._check_permission_for_company(company_id=company_id, user_id=user_id)

        query = select(QuizResultModel).filter_by(company_id=company_id)
        if quiz_user_id:
            query = query.filter_by(user_id=quiz_user_id)
        if quiz_id:
            query = query.filter_by(quiz_id=quiz_id)
        quiz_results = await self.db.execute(query)
        quiz_results = quiz_results.scalars().all()
        return [QuizResult.from_orm(quiz_result) for quiz_result in quiz_results]

    async def _get_answers_for_company(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: int,
            quiz_id: int
    ) -> List[UploadQuizAnswersForCompany]:
        await self._check_permission_for_company(company_id=company_id, user_id=user_id)

        find_keys = f'company_id:{company_id}'
        if quiz_user_id:
            find_keys = f'user_id:{quiz_user_id}_' + find_keys
        if quiz_id:
            find_keys = find_keys + f'_quiz_id:{quiz_id}'
        keys = await self.db_redis.keys(f'*{find_keys}*')
        answers = []
        for key in keys:
            questions = json.loads(await self.db_redis.get(key))
            for question in questions:
                answers.append(
                    UploadQuizAnswersForCompany(
                        user_id=key[self.find_index(key, 'user_id'): self.find_index(key, 'user_id') + 1],
                        quiz_id=key[self.find_index(key, 'quiz_id'):],
                        question=question,
                        answers=', '.join(questions.get(question))
                    )
                )

        return answers

    """Upload quiz results for user"""
    async def get_quiz_results_for_user(
            self,
            id: int,
            user_id: int,
            company_id: Optional[int] = None,
            quiz_id: Optional[int] = None
    ) -> List[QuizResult]:
        return await self._get_quiz_results_for_user(
            id=id,
            user_id=user_id,
            company_id=company_id,
            quiz_id=quiz_id
        )

    """Export to CSV quiz results for user"""
    async def export_results_for_user(
            self,
            id: int,
            user_id: int,
            company_id: Optional[int] = None,
            quiz_id: Optional[int] = None,
            filename: Optional[str] = "export"
    ) -> StreamingResponse:
        results = await self._get_quiz_results_for_user(
            id=id,
            user_id=user_id,
            company_id=company_id,
            quiz_id=quiz_id
        )

        export = self._export_to_csv(values=results, filename=filename)
        return export

    """Upload answers for user"""
    async def get_quiz_answers_for_user(
            self,
            id: int,
            user_id: int,
            company_id: Optional[int] = None,
            quiz_id: Optional[int] = None,
    ) -> List[UploadQuizAnswersForUser]:
        return await self._get_quiz_answers_for_user(
            id=id,
            user_id=user_id,
            company_id=company_id,
            quiz_id=quiz_id
        )

    """Export to CSV answers for user"""
    async def export_answers_for_user(
            self,
            id: int,
            user_id: int,
            company_id: Optional[int] = None,
            quiz_id: Optional[int] = None,
            filename: Optional[str] = "export"
    ) -> StreamingResponse:
        results = await self._get_quiz_answers_for_user(
            id=id,
            user_id=user_id,
            company_id=company_id,
            quiz_id=quiz_id
        )

        export = self._export_to_csv(values=results, filename=filename)
        return export

    """Upload quiz results for company"""
    async def get_quiz_results_for_company(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: Optional[int] = None,
            quiz_id: Optional[int] = None
    ) -> List[QuizResult]:
        return await self._get_quiz_results_for_company(
            company_id=company_id,
            user_id=user_id,
            quiz_user_id=quiz_user_id,
            quiz_id=quiz_id
        )

    """Export to CSV quiz results for company"""
    async def export_quiz_results_for_company(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: Optional[int] = None,
            quiz_id: Optional[int] = None,
            filename: Optional[str] = "export"
    ) -> StreamingResponse:
        results = await self._get_quiz_results_for_company(
            company_id=company_id,
            user_id=user_id,
            quiz_user_id=quiz_user_id,
            quiz_id=quiz_id
        )
        export = self._export_to_csv(values=results, filename=filename)
        return export

    """Upload quiz answers for company"""
    async def get_answers_for_company(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: int,
            quiz_id: int
    ) -> List[UploadQuizAnswersForCompany]:
        return await self._get_answers_for_company(
            company_id=company_id,
            user_id=user_id,
            quiz_user_id=quiz_user_id,
            quiz_id=quiz_id
        )

    """Export to CSV quiz answers for company"""
    async def export_quiz_answers_for_company(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: Optional[int] = None,
            quiz_id: Optional[int] = None,
            filename: Optional[str] = "export"
    ) -> StreamingResponse:
        results = await self._get_answers_for_company(
            company_id=company_id,
            user_id=user_id,
            quiz_user_id=quiz_user_id,
            quiz_id=quiz_id
        )
        export = self._export_to_csv(values=results, filename=filename)
        return export
