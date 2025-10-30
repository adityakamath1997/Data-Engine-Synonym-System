from pydantic_settings import BaseSettings
from typing import Literal


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
    
    cache_strategy: Literal["redis", "memory"]
    cache_ttl: int
    
    class Config:
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        return f"mssql+pyodbc://{self.database_user}:{self.database_password}@{self.database_server}:{self.database_port}/{self.database_name}?driver={self.database_driver.replace(' ', '+')}&TrustServerCertificate=yes"


settings = Settings()

