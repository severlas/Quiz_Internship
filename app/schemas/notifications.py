from pydantic import BaseModel
from typing import Optional


class NotificationMessage(BaseModel):
    message: Optional[str] = "Notification sent in the background"

    class Config:
        orm_mode = True
