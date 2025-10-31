from enum import Enum

from pydantic_settings import BaseSettings


class CacheStrategy(str, Enum):
    REDIS = "redis"
    MEMORY = "memory"


class Settings(BaseSettings):
    database_server: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    database_driver: str

    redis_host: str
    redis_port: int
    redis_db: int

    cache_strategy: CacheStrategy
    cache_ttl: int

    class Config:
        case_sensitive = False

    @property
    def database_url(self):
        driver = self.database_driver.replace(" ", "+")
        return (
            f"mssql+pyodbc://{self.database_user}:{self.database_password}"
            f"@{self.database_server}:{self.database_port}/{self.database_name}"
            f"?driver={driver}&TrustServerCertificate=yes"
        )


settings = Settings()
