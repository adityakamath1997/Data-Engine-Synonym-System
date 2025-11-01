from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheStrategy(ABC):
    """Abstract base for all cache implementations."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache, returns None if not found or expired."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> None:
        """Store value in cache with TTL in seconds."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove key from cache."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists and hasn't expired."""
        pass

    @abstractmethod
    def get_info(self) -> Any:
        """Return metadata about the cache backend."""
        pass
