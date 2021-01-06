import asyncio

import typer

from backend.config import load_configuration
from backend.db import get_engine
from backend.models import Base

app = typer.Typer()


async def init_database():
    config = load_configuration()
    engine = get_engine(config.database)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.command()
def dummy():
    typer.echo("Dummy command")


@app.command()
def initdb():
    asyncio.run(init_database())
    typer.echo("Database was created")


if __name__ == "__main__":
    app()
