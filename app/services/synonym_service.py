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

        cached = self.cache.get(cache_key)

        if cached:
            elapsed = (time.time() - start) * 1000
            logger.info(
                f"{Fore.GREEN}[CACHE HIT - {cache_source}]{Style.RESET_ALL} "
                f"Retrieved from cache in {Fore.CYAN}{elapsed:.2f}ms{Style.RESET_ALL}"
            )

            metadata = CacheMetadata(from_cache=True, cache_info=cache_info)
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

        self.cache.set(cache_key, data, settings.cache_ttl)

        elapsed = (time.time() - start) * 1000
        logger.info(
            f"{Fore.RED}[DATABASE]{Style.RESET_ALL} "
            f"Retrieved from database in {Fore.CYAN}{elapsed:.2f}ms{Style.RESET_ALL}"
        )

        metadata = CacheMetadata(from_cache=False)
        return [SynonymResponse(**item, cache_metadata=metadata) for item in data]
