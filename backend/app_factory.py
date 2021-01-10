from typing import Callable, Coroutine, cast

from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from backend.cache.utils import get_cache_backend
from backend.config import Configuration, setup_sentry
from backend.db.utils import get_engine
from backend.logging import setup_logging
from backend.routes import api_router
from backend.types import AppState, BaseError
from backend.utils import base_error_handler


class BackendApp(FastAPI):
    state: AppState  # type: ignore


def create_startup_hook(app: BackendApp) -> Callable[[], Coroutine[None, None, None]]:
    async def startup_hook() -> None:
        app.state.cache = await get_cache_backend(app.state.config.cache)
        app.state.engine = get_engine(app.state.config.database)

    return startup_hook


def create_shutdown_hook(app: BackendApp) -> Callable[[], Coroutine[None, None, None]]:
    async def shutdown_hook() -> None:
        if app.state.cache is not None:
            app.state.cache.close()
            await app.state.cache.wait_closed()
        if app.state.engine is not None:
            await app.state.engine.dispose()

    return shutdown_hook


exception_handlers = {BaseError: base_error_handler}


def create_app(config: Configuration) -> BackendApp:
    setup_logging(config)
    setup_sentry(config)

    app = cast(
        BackendApp,
        FastAPI(
            title="GraphQLBackend",
            description="GraphQL App backend",
            debug=config.debug,
            exception_handlers=exception_handlers,  # type: ignore
        ),
    )
    app.state.config = config

    app.include_router(api_router)

    app.router.add_event_handler("startup", create_startup_hook(app))
    app.router.add_event_handler("shutdown", create_shutdown_hook(app))

    app.add_middleware(ProxyHeadersMiddleware)
    app.add_middleware(SentryAsgiMiddleware)

    return app
