from typing import List

from sqlalchemy.orm import Session

from app.cache.factory import CacheFactory
from app.config import settings
from app.database.repository import SynonymRepository
from app.models.synonym import SynonymResponse


class SynonymService:
    def __init__(self, session: Session):
        self.repo = SynonymRepository(session)
        self.cache = CacheFactory.get_cache()

    def get_all(self) -> List[SynonymResponse]:
        cache_key = "synonyms:all"
        cached = self.cache.get(cache_key)

        if cached:
            return [SynonymResponse(**item, from_cache=True) for item in cached]

        synonyms = self.repo.get_all()
        data = [
            {
                "word_id": s.word_id,
                "word": s.word,
                "synonyms": s.synonyms,
            }
            for s in synonyms
        ]

        self.cache.set(cache_key, data, settings.cache_ttl)

        return [SynonymResponse(**item, from_cache=False) for item in data]
