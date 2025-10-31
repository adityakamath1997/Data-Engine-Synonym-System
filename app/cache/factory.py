from app.cache.base import CacheStrategy
from app.cache.memory_cache import MemoryCache
from app.cache.redis_cache import RedisCache
from app.config import CacheStrategy as CacheStrategyEnum
from app.config import settings


class CacheFactory:
    _instance = None

    @classmethod
    def get_cache(cls) -> CacheStrategy:
        if cls._instance is None:
            if settings.cache_strategy == CacheStrategyEnum.REDIS:
                cls._instance = RedisCache()
            elif settings.cache_strategy == CacheStrategyEnum.MEMORY:
                cls._instance = MemoryCache()
            else:
                raise ValueError(f"Unknown cache strategy: {settings.cache_strategy}")
        return cls._instance
