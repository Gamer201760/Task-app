import os
from logging import getLogger

import ydb

logger = getLogger(__name__)

endpoint = os.getenv('YDB_ENDPOINT')
database = os.getenv('YDB_DATABASE', '/local')
driver = ydb.aio.Driver(
    endpoint=endpoint,
    database=database,
    credentials=ydb.credentials_from_env_variables())

pool = ydb.aio.SessionPool(driver, size=10)


async def connect():
    logger.info(f'connect to {endpoint}{database}')
    await driver.wait(timeout=10)


def getDriver() -> ydb.aio.Driver:
    return driver


def getPool() -> ydb.aio.SessionPool:
    return pool
