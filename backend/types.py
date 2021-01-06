from typing import Any

from aioredis.commands import Redis
from backend.config import Configuration


class AppState:
    cache: Redis
    config: Configuration


class BaseError(Exception):
    message = "Unexpected exception"
    code = "unexpected_exception"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(self.message)
