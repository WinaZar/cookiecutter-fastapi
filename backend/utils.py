import asyncio
from typing import List, Coroutine, Any

from backend.types import BaseError
from starlette.responses import JSONResponse
from starlette.requests import Request


async def base_error_handler(request: Request, exception: BaseError) -> JSONResponse:
    status_code = getattr(exception, "status_code", 500)

    return JSONResponse(
        {"code": exception.code, "message": exception.message}, status_code=status_code
    )


async def gather_with_concurrency(
    count: int, tasks: List[Coroutine[Any, Any, Any]]
) -> List[Any]:
    semaphore = asyncio.Semaphore(count)

    async def semaphore_task(task: Coroutine[Any, Any, Any]) -> Any:
        async with semaphore:
            return await task

    result: List[Any] = await asyncio.gather(
        *(semaphore_task(task) for task in tasks), return_exceptions=True
    )

    return result
