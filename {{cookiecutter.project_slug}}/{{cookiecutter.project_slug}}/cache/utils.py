from aioredis import Redis, from_url

from {{cookiecutter.project_slug}}.config import CacheConfiguration


def get_cache_backend(config: CacheConfiguration) -> Redis:
    connection: Redis = from_url(  # type: ignore
        config.dsn, encoding="utf-8", decode_responses=True
    )
    return connection
