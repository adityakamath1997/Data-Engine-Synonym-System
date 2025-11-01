from threading import Lock

from app.cache.base import CacheStrategy
from app.cache.memory_cache import MemoryCache
from app.cache.redis_cache import RedisCache
from app.config import CacheStrategy as CacheStrategyEnum
from app.config import settings


class CacheFactory:
    """
    Singleton factory for creating cache instances.

    The cache strategy is determined by the CACHE_STRATEGY environment variable.
    """

    _instance = None
    _lock = Lock()

    @classmethod
    def get_cache(cls) -> CacheStrategy:
        """Returns the configured cache instance (Redis or Memory)."""
        if cls._instance is None:
            with cls._lock:
                # Double-check to avoid race conditions
                if cls._instance is None:
                    if settings.cache_strategy == CacheStrategyEnum.REDIS:
                        cls._instance = RedisCache()
                    elif settings.cache_strategy == CacheStrategyEnum.MEMORY:
                        cls._instance = MemoryCache()
                    else:
                        raise ValueError(
                            f"Unknown cache strategy: {settings.cache_strategy}"
                        )
        return cls._instance
