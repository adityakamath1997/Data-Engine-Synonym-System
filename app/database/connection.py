from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    pool_size=10,  # Base pool size
    max_overflow=20,  # Extra connections allowed under load
    pool_pre_ping=True,  # Test connection before use (handles disconnects)
)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    """FastAPI dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Returns connection to pool
