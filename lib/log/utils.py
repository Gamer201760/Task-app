import datetime
import json
import logging
import traceback

from pydantic import BaseModel
from starlette.responses import StreamingResponse


def write_log(msg):
    print(msg)


class BaseJsonLogSchema(BaseModel):
    thread: int | None
    level: str
    level_code: int
    message: str
    source: str
    timestamp: str
    duration: float
    exceptions: list[str] | str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    parent_id: str | None = None


class JsonLogSchema(BaseModel):
    client_ip: str | None
    path: str | None
    req_headers: dict | None
    res_headers: dict | None
    status_code: int | None


LEVEL_TO_NAME = logging._levelToName.copy()


class JSONLogFormatter(logging.Formatter):
    """
    Кастомизированный класс-форматер для логов в формате json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Преобразование объект журнала в json

        :param record: объект журнала
        :return: строка журнала в JSON формате
        """
        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        """
        Перевод записи объекта журнала
        в json формат с необходимым перечнем полей

        :param record: объект журнала
        :return: Словарь с объектами журнала
        """
        now = datetime \
            .datetime \
            .fromtimestamp(record.created) \
            .astimezone() \
            .replace(microsecond=0) \
            .isoformat()

        message = record.getMessage()
        duration = record.msecs

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level_code=record.levelno,
            level=LEVEL_TO_NAME[record.levelno],
            message=message,
            source=record.name,
            duration=duration
        )

        if record.exc_info:
            json_log_fields.exceptions = \
                traceback.format_exception(*record.exc_info)

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        json_log_object = json_log_fields.model_dump(
            exclude_unset=True,
            by_alias=True,
        )

        if isinstance(record.args, dict):
            req = record.args.get('request', None)
            res: StreamingResponse = record.args.get('response', None)
            if req and res:
                log = JsonLogSchema(
                    client_ip=req.get('client', [])[0],
                    path=req.get('path'),
                    req_headers=req.headers,
                    res_headers=dict(res.headers),
                    status_code=res.status_code
                )
                json_log_object.update(log.model_dump())

        return json_log_object
