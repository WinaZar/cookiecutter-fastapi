import os
from pathlib import Path
from typing import Literal, Optional, cast

import sentry_sdk
from pydantic import BaseModel, RedisDsn, StrictStr, HttpUrl, PositiveInt
from dynaconf import Dynaconf

APP_ENV = Literal["development", "testing", "production"]
PROJECT_ROOT = Path(__file__).parent.parent


class CacheConfiguration(BaseModel):
    dsn: RedisDsn


class ServerConfiguration(BaseModel):
    host: StrictStr
    port: PositiveInt


class Configuration(BaseModel):
    cache: CacheConfiguration
    server: ServerConfiguration
    environment: StrictStr
    sentry_dsn: Optional[HttpUrl]
    debug: bool


def load_configuration(env: Optional[APP_ENV] = None) -> Configuration:
    if not env:
        env = cast(APP_ENV, os.getenv("ENV_FOR_DYNACONF", "development"))

    settings = Dynaconf(
        settings_files=["default.yaml", f"{env}.yaml", ".secrets.yaml"],
        load_dotenv=True,
        merge_enabled=True,
        root_path=str(PROJECT_ROOT / "config"),
        envvar_prefix="MYPROJECT",
    )

    config_dict = {"environment": env}
    for key in Configuration.__fields__.keys():
        if settings.get(key) is not None:
            config_dict[key] = settings[key]

    config = Configuration(**config_dict)

    return config


def dump_config(config: Configuration) -> str:
    return config.json(indent=2, sort_keys=True)


def setup_sentry(config: Configuration) -> None:
    if config.sentry_dsn:
        sentry_sdk.init(dsn=config.sentry_dsn, environment=config.environment)
