import secrets
from datetime import datetime, timezone

from fastapi import Header, HTTPException

from app.database import database, api_keys


def generate_api_key() -> str:
    return f"bk_{secrets.token_hex(16)}"


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    query = api_keys.select().where(api_keys.c.key == x_api_key)
    row = await database.fetch_one(query)

    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key")

    update = (
        api_keys.update()
        .where(api_keys.c.key == x_api_key)
        .values(
            request_count=row._mapping["request_count"] + 1,
            last_request=datetime.now(timezone.utc),
        )
    )
    await database.execute(update)

    return x_api_key
