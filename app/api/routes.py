from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database.connection import get_db
from app.models.synonym import SynonymResponse
from app.services.synonym_service import SynonymService

router = APIRouter()


@router.get("/info")
def get_info():
    """Returns cache config (strategy and TTL)."""
    return {
        "cache_strategy": settings.cache_strategy.value,
        "cache_ttl_seconds": settings.cache_ttl,
    }


@router.get("/synonyms", response_model=List[SynonymResponse])
def get_synonyms(db: Session = Depends(get_db)):
    """Get all synonyms with cache metadata showing hits/misses."""
    service = SynonymService(db)
    return service.get_all()
