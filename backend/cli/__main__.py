import asyncio

import typer
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.auth.utils import create_user
from backend.config import load_configuration
from backend.db.models import Base
from backend.db.utils import get_engine

app = typer.Typer()


async def _init_database() -> None:
    config = load_configuration()
    engine = get_engine(config.database)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def _create_user(username: str, password: str) -> None:
    config = load_configuration()
    engine = get_engine(config.database)
    async with AsyncSession(engine) as session:
        await session.run_sync(create_user, username, password)


@app.command()
def dummy() -> None:
    typer.echo("Dummy command")


@app.command()
def create_new_user(username: str, password: str) -> None:
    asyncio.run(_create_user(username, password))
    typer.echo("New user was created")


if __name__ == "__main__":
    app()
