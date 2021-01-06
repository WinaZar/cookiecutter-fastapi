from typing import cast

from aioredis.commands import Redis
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import Request

from backend.config import Configuration
from backend.types import AppState


async def get_cache(request: Request) -> Redis:
    state = cast(AppState, request.app.state)

    return state.cache


async def get_session(request: Request) -> AsyncSession:
    state = cast(AppState, request.app.state)

    async with AsyncSession(state.engine) as session:
        yield session


async def get_config(request: Request) -> Configuration:
    state = cast(AppState, request.app.state)

    return state.config
