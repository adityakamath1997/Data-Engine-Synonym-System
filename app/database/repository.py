from typing import List

from sqlalchemy.orm import Session

from app.models.synonym import Synonym


class SynonymRepository:
    """Repository for synonym data access."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Synonym]:
        """Get all synonyms from the database."""
        return self.session.query(Synonym).all()
