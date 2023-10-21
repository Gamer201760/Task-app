import asyncio

from lib.ydb import getPool

from .task import create_table as create_task_table

tables = [
    create_task_table
]

async def create_table():
    coros = [
        getPool().retry_operation(table) for table in tables
    ]

    await asyncio.gather(*coros)
