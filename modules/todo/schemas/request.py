from datetime import datetime

from pydantic import BaseModel, field_serializer


class TaskRequestSchema(BaseModel):
    text: str
    deadline: datetime
    completed: bool = False

    @field_serializer('deadline')
    def ser_deadline(self, deadline: datetime) -> int:
        return int(deadline.timestamp())


class TaskRequestUpdateSchema(BaseModel):
    text: str | None = None
    deadline: datetime | None = None
    completed: bool | None = None

    @field_serializer('deadline')
    def ser_deadline(self, deadline: datetime) -> int:
        return int(deadline.timestamp())
