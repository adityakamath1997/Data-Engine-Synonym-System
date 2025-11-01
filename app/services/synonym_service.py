import logging
import time
from typing import List

from colorama import Fore, Style
from sqlalchemy.orm import Session

from app.cache.factory import CacheFactory
from app.config import settings
from app.database.repository import SynonymRepository
from app.models.synonym import CacheMetadata, SynonymResponse

# Setting up the logger
logger = logging.getLogger(__name__)


class SynonymService:
    """Handles synonym retrieval with caching."""

    def __init__(self, session: Session):
        self.repo = SynonymRepository(session)
        self.cache = CacheFactory.get_cache()

    def get_all(self) -> List[SynonymResponse]:
        """Get all synonyms, checking cache before hitting the database."""
        start = time.time()
        cache_key = "synonyms:all"
        cache_info = self.cache.get_info()
        cache_source = cache_info.cache_source.upper()

        # Try cache first, but fall back to DB if it fails
        cached = None
        try:
            cached = self.cache.get(cache_key)
        except Exception as e:
            logger.warning(f"Cache get failed: {e}")

        if cached:
            elapsed = (time.time() - start) * 1000
            logger.info(
                f"{Fore.GREEN}[CACHE HIT - {cache_source}]{Style.RESET_ALL} "
                f"Retrieved from cache in {Fore.CYAN}{elapsed:.2f}ms{Style.RESET_ALL}"
            )

            metadata = CacheMetadata(
                from_cache=True, cache_info=cache_info, response_time_ms=elapsed
            )
            return [SynonymResponse(**item, cache_metadata=metadata) for item in cached]

        logger.info(
            f"{Fore.YELLOW}[CACHE MISS - {cache_source}]{Style.RESET_ALL} "
            f"Querying database..."
        )

        synonyms = self.repo.get_all()

        # Convert to dicts to avoid SQLAlchemy serialization issues
        data = [
            {
                "word_id": s.word_id,
                "word": s.word,
                "synonyms": s.synonyms,
            }
            for s in synonyms
        ]

        # Try to cache for next time, but don't fail the request if caching fails
        try:
            self.cache.set(cache_key, data, settings.cache_ttl)
        except Exception as e:
            logger.warning(f"Cache set failed: {e}")

        elapsed = (time.time() - start) * 1000
        logger.info(
            f"{Fore.RED}[DATABASE]{Style.RESET_ALL} "
            f"Retrieved from database in {Fore.CYAN}{elapsed:.2f}ms{Style.RESET_ALL}"
        )

        metadata = CacheMetadata(from_cache=False, response_time_ms=elapsed)
        return [SynonymResponse(**item, cache_metadata=metadata) for item in data]
