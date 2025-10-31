import time
from threading import Lock
from typing import Any, Optional

from app.cache.base import CacheStrategy
from app.models.synonym import CacheInfo


class MemoryCache(CacheStrategy):
    def __init__(self):
        self._data = {}
        self._lock = Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._data:
                return None

            value, expires_at = self._data[key]

            if time.time() > expires_at:
                del self._data[key]
                return None

            return value

    def set(self, key: str, value: Any, ttl: int) -> None:
        expires_at = time.time() + ttl
        with self._lock:
            self._data[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)

    def exists(self, key: str) -> bool:
        with self._lock:
            if key not in self._data:
                return False

            _, expires_at = self._data[key]

            if time.time() > expires_at:
                del self._data[key]
                return False

            return True

    def get_info(self) -> CacheInfo:
        return CacheInfo(cache_source="memory")
