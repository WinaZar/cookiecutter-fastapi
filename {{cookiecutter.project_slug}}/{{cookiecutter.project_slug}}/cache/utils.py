from aioredis import from_url, Redis
from aioredis.commands import Redis

from {{cookiecutter.project_slug}}.config import CacheConfiguration


def get_cache_backend(config: CacheConfiguration) -> Redis:
    connection = from_url(
        config.dsn, encoding="utf-8", decode_responses=True
    )
    return connection
