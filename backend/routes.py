from typing import Dict

from fastapi import APIRouter, Depends, Request
from graphql.execution.executors.asyncio import AsyncioExecutor
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.graphql import GraphQLApp
from starlette.responses import PlainTextResponse

from backend.dependencies import get_session
from backend.models import User
from backend.schema import schema

api_router = APIRouter()
graphql_app = GraphQLApp(schema=schema, executor_class=AsyncioExecutor)


@api_router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    return "pong"


@api_router.api_route("/graphql", methods=["GET", "POST"])
async def graphql_endpoint(request: Request):
    return await graphql_app.handle_graphql(request)


@api_router.post("/add_test_user")
async def add_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> Dict[str, str]:
    async with session.begin():
        session.add(User(name="Josh"))
    await session.commit()

    return {"message": "Job done"}
