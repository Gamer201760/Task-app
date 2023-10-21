import uuid
from logging import getLogger

import ydb
import ydb.aio

from lib.ydb import database, getPool
from lib.ydb.exceptions import DatabaseError
from lib.ydb.literals import Operator
from lib.ydb.query import YdbQuery

logger = getLogger(__name__)


class YbdMixin(YdbQuery):
    table: str
    pool: ydb.aio.SessionPool = getPool()
    database = database

    async def upsert(self, data: dict) -> uuid.UUID:
        return await self._sert_base(data, self.generate_upsert)

    async def insert(self, data: dict) -> uuid.UUID:
        return await self._sert_base(data, self.generate_insert)

    async def _sert_base(self, data: dict, generate_func) -> uuid.UUID:
        id = uuid.uuid4()
        payload = {
            'id': str(id).encode(),
        }
        payload.update(data)
        payload = self._transform_payload(payload)

        query = generate_func(payload)
        await self.execute(query, payload)
        return payload['$id']

    async def update(self, conditions: dict, payload: dict):
        payload = self._transform_payload(payload)
        conditions = self._transform_payload(conditions)

        query = self.generate_update(conditions, payload)
        await self.execute(query, payload | conditions)
        return True

    async def read(
        self,
        payload: dict | None,
        operation: Operator | None
    ) -> list[dict] | None:
        if payload:
            payload = self._transform_payload(payload)
        query = self.generate_select(payload, operation)
        return await self.execute(query, payload)

    async def remove(self, payload: dict):
        payload = self._transform_payload(payload)
        query = self.generate_delete(payload)
        return await self.execute(query, payload)

    async def execute(
        self,
        query: str,
        payload: dict | None
    ):
        try:
            return await self.pool.retry_operation(
                self.transaction,
                query,
                payload
            )
        except ydb.Error as e:
            logger.error(e.issues)
            raise DatabaseError()

    async def transaction(
        self,
        session: ydb.Session,
        query: str,
        payload: dict
    ) -> list[dict] | None:
        prepare: ydb.DataQuery = await session.prepare(query)
        t = await session.transaction(ydb.SerializableReadWrite()).execute(
            prepare,
            payload,
            commit_tx=True,
        )
        if len(t) == 0:
            return None

        return t[-1].rows

    def _transform_payload(self, payload: dict) -> dict:
        return {'$' + key: value.encode() if isinstance(value, str)
                else value for key, value in payload.items()}
