from typing import cast

from aioredis.commands import Redis
from fastapi import Request

from backend.types import AppState


async def get_cache(request: Request) -> Redis:
    state = cast(AppState, request.app.state)

    return state.cache
