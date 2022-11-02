from typing import List, Optional
from sqlalchemy import select, distinct, asc, func, desc
from app.services.baseservice import BaseService
from app.services.exceptions import NotFoundError, PermissionError
from app.models.quiz_results import QuizResultModel
from app.schemas.analytics import AnalyticsGPAByQuiz, AnalyticsGPAForCompany, GPAOverTime, GPAByQuiz


class AnalyticsService(BaseService):
    """Analytics"""

    @staticmethod
    async def _get_gpa_by_quiz(quiz_results: List[QuizResultModel]) -> List[AnalyticsGPAByQuiz]:
        analytics = []
        quizzes_id = []
        for quiz_result in quiz_results:
            if quiz_result.quiz_id not in quizzes_id:
                quizzes_id.append(quiz_result.quiz_id)
                analytics_gpa = AnalyticsGPAByQuiz(
                    quiz_id=quiz_result.quiz_id,
                    gpa_over_time=[]
                )
                analytics.append(analytics_gpa)
            gpa_over_time = GPAByQuiz(
                gpa_by_quiz=quiz_result.gpa_by_quiz,
                created_at=quiz_result.created_at
            )
            analytics_gpa.gpa_over_time.append(gpa_over_time)
        return analytics

    async def _check_permission_for_company(self, company_id: int, user_id: int) -> PermissionError:
        admins = await self._get_admins_by_company_id(company_id)

        if user_id not in admins:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to get information about company with id:{company_id}!"
            )

    """Get list of GPA users over time"""
    async def get_gpa_for_company(
            self,
            company_id: int,
            user_id: int,
    ) -> List[AnalyticsGPAForCompany]:
        await self._check_permission_for_company(company_id=company_id, user_id=user_id)
        quiz_results = await self.db.execute(select(QuizResultModel).filter_by(company_id=company_id))
        quiz_results = quiz_results.scalars().all()
        analytics = []
        users_id = []
        for quiz_result in quiz_results:
            if quiz_result.user_id not in users_id:
                users_id.append(quiz_result.user_id)
                analytics_gpa = AnalyticsGPAForCompany(
                    user_id=quiz_result.user_id,
                    gpa_over_time=[]
                )
                analytics.append(analytics_gpa)
            gpa_over_time = GPAOverTime(
                gpa_all=quiz_result.gpa_all,
                created_at=quiz_result.created_at
            )
            analytics_gpa.gpa_over_time.append(gpa_over_time)

        return analytics

    """Get list of GPA user by quiz over time"""
    async def get_gpa_by_quiz(
            self,
            company_id: int,
            user_id: int,
            quiz_user_id: int
    ) -> List[AnalyticsGPAByQuiz]:
        await self._check_permission_for_company(company_id=company_id, user_id=user_id)
        quiz_results = await self.db.execute(
            select(QuizResultModel).
            filter_by(company_id=company_id, user_id=quiz_user_id)
        )
        quiz_results = quiz_results.scalars().all()
        analytics = await self._get_gpa_by_quiz(quiz_results=quiz_results)

        return analytics

    """Get users and time of last take to quiz"""
    async def get_users_and_time_of_last_quiz(
            self,
            company_id: int,
            user_id: int,
    ) -> List[QuizResultModel]:
        await self._check_permission_for_company(company_id=company_id, user_id=user_id)
        query = select(QuizResultModel).filter_by(company_id=company_id).order_by(desc(QuizResultModel.id))
        quiz_results = await self.db.execute(query)
        quiz_results = quiz_results.scalars().all()
        users_id = []
        response_data = []
        for quiz_result in quiz_results:
            if quiz_result.user_id not in users_id:
                users_id.append(quiz_result.user_id)
                response_data.append(quiz_result)
        return response_data

    """Get GPA for all quizzes"""
    async def get_gpa_for_user(self, id: int) -> QuizResultModel:
        quiz_results = await self.db.execute(select(QuizResultModel).filter_by(user_id=id))
        quiz_results = quiz_results.scalars().all()
        return quiz_results[-1]

    """Get list GPA by quizzes"""
    async def get_gpa_by_quiz_for_user(
            self,
            id: int,
            user_id: int,
    ) -> List[AnalyticsGPAByQuiz]:
        if user_id != id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to get information about user with id:{id}!"
            )
        quiz_results = await self.db.execute(select(QuizResultModel).filter_by(user_id=id))
        quiz_results = quiz_results.scalars().all()
        analytics = await self._get_gpa_by_quiz(quiz_results=quiz_results)
        return analytics

    """Get list quiz and time of last take quiz"""
    async def get_quizzes_and_time_of_last_quiz(
            self,
            id: int,
            user_id: int
    ) -> List[QuizResultModel]:
        if user_id != id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to get information about user with id:{id}"
            )
        quiz_results = await self.db.execute(
            select(QuizResultModel).
            filter_by(user_id=id).
            order_by(desc(QuizResultModel.id))
        )
        quiz_results = quiz_results.scalars().all()
        quizzes_id = []
        response_data = []
        for quiz_result in quiz_results:
            if quiz_result.quiz_id not in quizzes_id:
                quizzes_id.append(quiz_result.quiz_id)
                response_data.append(quiz_result)
        return response_data

