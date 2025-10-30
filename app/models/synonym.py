from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Synonym(SQLModel, table=True):
    __tablename__ = "synonyms"

    word_id: Optional[int] = Field(
        default=None, primary_key=True
    )  # Database generates word_id automatically
    word: str
    synonyms: str


class SynonymResponse(BaseModel):
    word_id: int
    word: str
    synonyms: str
    from_cache: bool
