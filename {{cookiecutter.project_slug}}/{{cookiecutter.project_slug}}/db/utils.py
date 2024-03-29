from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from {{cookiecutter.project_slug}}.config import DatabaseConfiguration


def get_engine(config: DatabaseConfiguration) -> AsyncEngine:
    return create_async_engine(config.dsn)
