from typing import cast

from fastapi import Request

from {{cookiecutter.project_slug}}.config import Configuration
from {{cookiecutter.project_slug}}.types import AppState


async def get_config(request: Request) -> Configuration:
    state = cast(AppState, request.app.state)

    return state.config
