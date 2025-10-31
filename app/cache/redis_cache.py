import json
from typing import Any, Optional

import redis

from app.cache.base import CacheStrategy
from app.config import settings
from app.models.synonym import CacheInfo


class RedisCache(CacheStrategy):
    """Distributed cache using Redis with JSON serialization."""

    def __init__(self):
        self.redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )
        self.host = settings.redis_host
        self.port = settings.redis_port

    def get(self, key: str) -> Optional[Any]:
        """Get and deserialize from Redis."""
        data = self.redis.get(key)
        if not data:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any, ttl: int) -> None:
        """Store with TTL using setex."""
        data = json.dumps(value)
        self.redis.setex(key, ttl, data)

    def delete(self, key: str) -> None:
        self.redis.delete(key)

    def exists(self, key: str) -> bool:
        """Check existence (returns count, so we check > 0)."""
        return self.redis.exists(key) > 0

    def get_info(self) -> CacheInfo:
        return CacheInfo(
            cache_source="redis",
            redis_host=self.host,
            redis_port=self.port,
        )
