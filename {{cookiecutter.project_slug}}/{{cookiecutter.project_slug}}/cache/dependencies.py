from typing import cast

from aioredis import Redis
from fastapi import Request

from {{cookiecutter.project_slug}}.types import AppState


async def get_cache(request: Request) -> Redis:
    state = cast(AppState, request.app.state)

    return state.cache
