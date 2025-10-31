from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Synonym(SQLModel, table=True):
    __tablename__ = "synonyms"

    word_id: Optional[int] = Field(
        default=None, primary_key=True
    )  # Since database generates word_id automatically
    word: str
    synonyms: str  # Comma-separated list stored as single string


class CacheInfo(BaseModel):
    """Info about which cache backend served the data."""

    cache_source: str  # "redis" or "memory"
    redis_host: Optional[str] = None
    redis_port: Optional[int] = None


class CacheMetadata(BaseModel):
    """Metadata indicating whether response came from cache or database."""

    from_cache: bool
    cache_info: Optional[CacheInfo] = None


class SynonymResponse(BaseModel):
    """API response model with synonym data + cache metadata."""

    word_id: int
    word: str
    synonyms: str
    cache_metadata: CacheMetadata
