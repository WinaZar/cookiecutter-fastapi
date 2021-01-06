from fastapi import APIRouter
from starlette.responses import PlainTextResponse


api_router = APIRouter()


@api_router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    return "pong"
