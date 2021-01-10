from aioredis import create_redis_pool
from aioredis.commands import Redis

from backend.config import CacheConfiguration


async def get_cache_backend(config: CacheConfiguration) -> Redis:
    connection = await create_redis_pool(config.dsn)
    return connection
