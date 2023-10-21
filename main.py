from logging import getLogger
from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from lib.log.config import LOG_CONFIG
from lib.ydb import connect, getDriver, getPool
from modules.todo.views import router as todo_router
from tables.table import create_table

dictConfig(LOG_CONFIG)

app = FastAPI()

logger = getLogger(__name__)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(todo_router, prefix='/api/v1')


@app.middleware('http')
async def req_logging(request: Request, call_next):
    response = await call_next(request)

    if int(request.headers.get('Content-lenght', 0)) < 1000:
        logger.debug('Logging', {'request': request, 'response': response})

    return response

@app.on_event('startup')
async def startup():
    await connect()
    await create_table()


@app.on_event('shutdown')
async def shutdown():
    await getPool().stop()
    await getDriver().stop()
