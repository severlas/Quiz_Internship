from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.notifications import NotificationMessage
from app.services.notifications import NotificationService

router = APIRouter(
    prefix='/notification',
    tags=['Notifications']
)


@router.get('/', response_model=NotificationMessage)
async def check_time_last_tested(
        background_tasks: BackgroundTasks,
        service: NotificationService = Depends(),

) -> NotificationMessage:
    background_tasks.add_task(service.send_email, users_email=await service.check_time_last_tested())
    return NotificationMessage()

