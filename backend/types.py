from typing import Any

from aioredis.commands import Redis
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from backend.config import Configuration


class AppState:
    cache: Redis
    config: Configuration
    engine: AsyncEngine


class BaseError(Exception):
    message = "Unexpected exception"
    code = "unexpected_exception"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(self.message)
