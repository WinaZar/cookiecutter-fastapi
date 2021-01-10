from typing import Dict

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from graphql.execution.executors.asyncio import AsyncioExecutor
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.graphql import GraphQLApp
from starlette.responses import PlainTextResponse

from backend.auth.dependencies import get_user
from backend.auth.utils import authenticate_user, generate_jwt
from backend.config import Configuration
from backend.db.dependencies import get_session
from backend.dependencies import get_config
from backend.schema import schema


class Token(BaseModel):
    access_token: str
    token_type: str


api_router = APIRouter()
graphql_app = GraphQLApp(schema=schema, executor_class=AsyncioExecutor)


@api_router.get(
    "/ping", response_class=PlainTextResponse, dependencies=[Depends(get_user)]
)
async def ping() -> str:
    return "pong"


@api_router.post("/token", response_model=Token)
async def obtain_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
    config: Configuration = Depends(get_config),
) -> Dict[str, str]:
    user = await session.run_sync(
        authenticate_user, form_data.username, form_data.password
    )
    token = generate_jwt(config, user)
    return {"access_token": token, "token_type": "bearer"}


@api_router.api_route(
    "/graphql", methods=["GET", "POST"], dependencies=[Depends(get_user)]
)
async def graphql_endpoint(request: Request) -> Response:
    return await graphql_app.handle_graphql(request)
