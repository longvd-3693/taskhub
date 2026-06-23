import json
import logging
import logging.config
from threading import Lock
from datetime import datetime, timezone

from app.core.config import settings


_RESERVED_FIELDS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


_LOGGING_CONFIGURED = False
_CONFIGURE_LOCK = Lock()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=timezone.utc,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        extra_fields = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _RESERVED_FIELDS
        }

        if extra_fields:
            payload.update(extra_fields)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    with _CONFIGURE_LOCK:
        if _LOGGING_CONFIGURED:
            return

        log_level = "DEBUG" if settings.debug else "INFO"

        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "json": {
                        "()": "app.core.logging.JsonFormatter",
                    },
                },
                "handlers": {
                    "default": {
                        "class": "logging.StreamHandler",
                        "formatter": "json",
                        "level": log_level,
                    },
                },
                "root": {
                    "handlers": ["default"],
                    "level": log_level,
                },
            }
        )
        _LOGGING_CONFIGURED = True
