from fastapi import APIRouter, Request
from starlette.responses import PlainTextResponse
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor

from backend.schema import schema


api_router = APIRouter()
graphql_app = GraphQLApp(schema=schema, executor_class=AsyncioExecutor)


@api_router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    return "pong"


@api_router.api_route("/graphql", methods=["GET", "POST"])
async def graphql_endpoint(request: Request):
    return await graphql_app.handle_graphql(request)
