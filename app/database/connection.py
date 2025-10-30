from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


class DatabaseConnection:
    def __init__(self):
        self.engine = create_engine(
            settings.database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


db_connection = DatabaseConnection()
