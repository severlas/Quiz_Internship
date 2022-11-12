from pydantic import BaseModel
from datetime import datetime


class BaseMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
