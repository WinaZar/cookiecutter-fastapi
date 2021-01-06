from __future__ import annotations
import sys
import logging
import loguru
from loguru import logger
from typing import Union

from backend.types import BaseError
from backend.config import Configuration


class InterceptLoguruHandler(logging.Handler):
    def __init__(self, stream: str = ""):
        del stream
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def exception_patcher(record: loguru.Record) -> None:
    record_exception = record["exception"]
    if (
        record_exception
        and record_exception.value
        and isinstance(record_exception.value, BaseError)
    ):
        record["extra"]["error_code"] = record_exception.value.code
        record["extra"]["error_message"] = record_exception.value.message


def setup_logging(config: Configuration) -> None:
    logging.basicConfig(handlers=[InterceptLoguruHandler()], level=0)

    if config.debug:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "level": "INFO",
                    "format": (
                        "<green>{time:YYYY-MM-DDTHH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
                        " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | "
                        "<level>{extra!s}</level>"
                    ),
                    "enqueue": True,
                },
            ],
            patcher=exception_patcher,
        )
    else:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "serialize": True,
                    "colorize": False,
                    "level": "INFO",
                    "enqueue": True,
                    "backtrace": False,
                }
            ],
            patcher=exception_patcher,
        )
