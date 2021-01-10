from typing import cast

from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.types import AppState


async def get_session(request: Request) -> AsyncSession:
    state = cast(AppState, request.app.state)

    async with AsyncSession(state.engine) as session:
        yield session
