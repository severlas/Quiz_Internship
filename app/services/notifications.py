from fastapi import BackgroundTasks
from app.services.baseservice import BaseService
from app.models.quiz_results import QuizResultModel
from app.models.users import UserModel
from typing import List
from sqlalchemy import select, desc
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from app.settings import settings
from log.config_log import logger


class NotificationService(BaseService):

    FREQUENCY_DAY = 7
    MESSAGE = "You haven't been tested in the last 7 days."
    EMAIL_HOST = settings.email_host
    EMAIL_HOST_SENDER = settings.email_host_sender
    EMAIL_HOST_PASSWORD = settings.email_host_password
    EMAIL_PORT = settings.email_port

    """Send email"""
    def send_email(self, users_email: list, message: str = MESSAGE) -> logger:
        server = smtplib.SMTP(host=self.EMAIL_HOST, port=self.EMAIL_PORT)
        server.starttls()
        try:
            server.login(user=self.EMAIL_HOST_SENDER, password=self.EMAIL_HOST_PASSWORD)
            msg = MIMEText(_text=message)
            for user_email in users_email:
                server.sendmail(from_addr=self.EMAIL_HOST_SENDER, to_addrs=user_email, msg=msg.as_string())
            return logger.info("Messages was sent successfully!")
        except Exception as ex:
            return logger.error(f"exceptions: {ex} detail='Messages wasn't sent. Check login and password!'")

    """Check time last tested"""
    async def check_time_last_tested(self) -> list:
        quiz_results = await self.db.execute(select(QuizResultModel).order_by(desc(QuizResultModel.id)))
        quiz_results = quiz_results.scalars().all()

        users_id = set([
            quiz_result.user_id for quiz_result in quiz_results
            if (datetime.now() - quiz_result.created_at.replace(tzinfo=None)).days >= self.FREQUENCY_DAY
        ])
        users_email = await self.db.execute(select(UserModel.email).filter(UserModel.id.in_(users_id)))
        users_email = users_email.scalars().all()
        return users_email

