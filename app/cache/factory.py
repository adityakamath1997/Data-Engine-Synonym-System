from app.cache.base import CacheStrategy
from app.cache.memory_cache import MemoryCache
from app.cache.redis_cache import RedisCache
from app.config import settings


def get_cache() -> CacheStrategy:
    strategy = settings.cache_strategy

    if strategy == "redis":
        return RedisCache()

    if strategy == "memory":
        return MemoryCache()

    raise ValueError(f"Unknown cache strategy: {strategy}")
