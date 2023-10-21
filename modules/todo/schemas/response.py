from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskResponeSchema(BaseModel):
    id: UUID
    text: str
    created_at: datetime
    deadline: datetime
    completed: bool
