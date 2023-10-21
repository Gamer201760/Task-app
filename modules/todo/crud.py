import logging
from uuid import UUID

from lib.exceptions import EntityNotFoundException
from lib.ydb.mixin import YbdMixin
from modules.todo.schemas.request import TaskRequestSchema, TaskRequestUpdateSchema

logger = logging.getLogger(__name__)


class Task(YbdMixin):
    table = 'task'

    async def create(self, task: TaskRequestSchema | TaskRequestUpdateSchema, id: UUID | None = None) -> dict:
        payload = task.model_dump(exclude_none=True)
        if id:
            payload.update({'id': str(id).encode()})
        else:
            payload.update({
                'created_at': {
                    'val': 'Cast(CurrentUtcDatetime() as Int32)',
                    'mode': 'var'
                }
            })
        return {'id': await self.upsert(payload)}

    async def get(self, **payload) -> list[dict]:
        obj = await self.read(payload, 'AND')
        if obj is None or len(obj) == 0:
            raise EntityNotFoundException()
        return obj

    async def delete(self, id: str) -> bool:
        await self.remove({
            'id': id
        })
        return True
