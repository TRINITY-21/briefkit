from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openweather_api_key: str = ""
    default_city: str = "Istanbul"
    crypto_coins: str = "bitcoin,ethereum,solana"
    database_url: str = "sqlite+aiosqlite:///./briefkit.db"
    rate_limit: str = "100/day"

    @property
    def async_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    class Config:
        env_file = ".env"


settings = Settings()
