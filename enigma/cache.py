from redis.asyncio import Redis

from enigma.config import get_config
from enigma.log import log


async def get_cache_value(key: str) -> bytes | None:
    redis = _get_redis()
    log.debug(f'Getting cache value "{key}"')
    try:
        value = await redis.get(key)
    except Exception as e:
        log.warn(f'Failed to get cache value "{key}": "{e}"')
        return None
    log.debug(f'Got cache value "{key}": "{value}"')
    return value


async def set_cache_value(key: str, value: bytes, ttl: int) -> None:
    redis = _get_redis()
    log.debug(f'Setting cache value "{key}" to "{value}" with TTL {ttl}s')
    try:
        await redis.set(key, value, ex=ttl)
        log.debug(f'Set cache value "{key}" to "{value}" with TTL {ttl}s')
    except Exception as e:
        log.warn(f'Failed to set cache value "{key}" to "{value}" with TTL {ttl}s: "{e}"')


# Private


_redis: Redis | None = None


def _get_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = _init_redis()
    return _redis


def _init_redis() -> Redis:
    cfg = get_config()
    log.info('Initializing Redis')
    redis = Redis(
        host=cfg.redis_host,
        port=cfg.redis_port,
        #username=cfg.redis_username,
        #password=cfg.redis_password,
    )
    log.info('Redis initialized')
    return redis
