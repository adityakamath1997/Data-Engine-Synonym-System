from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Synonym(SQLModel, table=True):
    __tablename__ = "synonyms"

    word_id: Optional[int] = Field(
        default=None, primary_key=True
    )  # Since database generates word_id automatically
    word: str
    synonyms: str


class CacheMetadata(BaseModel):
    from_cache: bool
    cache_source: Optional[str] = None
    redis_host: Optional[str] = None
    redis_port: Optional[int] = None


class SynonymResponse(BaseModel):
    word_id: int
    word: str
    synonyms: str
    cache_metadata: CacheMetadata
