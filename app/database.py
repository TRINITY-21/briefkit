import databases
import sqlalchemy
from datetime import datetime, timezone

from app.config import settings

database = databases.Database(settings.async_database_url)

metadata = sqlalchemy.MetaData()

api_keys = sqlalchemy.Table(
    "api_keys",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("key", sqlalchemy.String(64), unique=True, index=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=lambda: datetime.now(timezone.utc)),
    sqlalchemy.Column("request_count", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("last_request", sqlalchemy.DateTime, nullable=True),
)

# Create tables (sync engine for initial setup)
_sync_url = settings.async_database_url.replace("+aiosqlite", "").replace("+asyncpg", "")
engine = sqlalchemy.create_engine(_sync_url)
metadata.create_all(engine)
engine.dispose()
