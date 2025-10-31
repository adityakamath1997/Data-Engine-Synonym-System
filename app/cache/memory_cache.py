import time
from threading import Lock
from typing import Any, Optional

from app.cache.base import CacheStrategy
from app.models.synonym import CacheInfo


class MemoryCache(CacheStrategy):
    """Thread-safe in-memory cache using a dict."""

    def __init__(self):
        self._data = {}
        self._lock = Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get from cache, auto-deletes if expired."""
        with self._lock:
            if key not in self._data:
                return None

            value, expires_at = self._data[key]

            if time.time() > expires_at:
                del self._data[key]
                return None

            return value

    def set(self, key: str, value: Any, ttl: int) -> None:
        """Store with TTL in seconds. Calculates expiration before locking."""
        expires_at = time.time() + ttl
        with self._lock:
            self._data[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        """Remove key, safe if it doesn't exist."""
        with self._lock:
            self._data.pop(key, None)

    def exists(self, key: str) -> bool:
        """Check if key exists and is still valid."""
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
