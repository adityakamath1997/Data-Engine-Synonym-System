from app.cache.base import CacheStrategy
from app.cache.memory_cache import MemoryCache
from app.cache.redis_cache import RedisCache
from app.config import CacheStrategy as CacheStrategyEnum
from app.config import settings


def get_cache() -> CacheStrategy:
    if settings.cache_strategy == CacheStrategyEnum.REDIS:
        return RedisCache()

    if settings.cache_strategy == CacheStrategyEnum.MEMORY:
        return MemoryCache()

    raise ValueError(f"Unknown cache strategy: {settings.cache_strategy}")
