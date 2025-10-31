import json
from typing import Any, Optional

import redis

from app.cache.base import CacheStrategy
from app.config import settings


class RedisCache(CacheStrategy):
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.redis_host, port=settings.redis_port, decode_responses=True
        )

    def get(self, key: str) -> Optional[Any]:
        data = self.redis.get(key)
        if not data:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any, ttl: int) -> None:
        data = json.dumps(value)
        self.redis.setex(key, ttl, data)

    def delete(self, key: str) -> None:
        self.redis.delete(key)

    def exists(self, key: str) -> bool:
        return self.redis.exists(key) > 0
