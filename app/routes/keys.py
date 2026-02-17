from datetime import datetime, timezone

from fastapi import APIRouter

from app.auth import generate_api_key
from app.database import database, api_keys
from app.models import APIKeyResponse

router = APIRouter(prefix="/api", tags=["API Keys"])


@router.post("/keys", response_model=APIKeyResponse, status_code=201)
async def create_api_key():
    key = generate_api_key()
    now = datetime.now(timezone.utc)

    query = api_keys.insert().values(
        key=key,
        created_at=now,
        request_count=0,
    )
    await database.execute(query)

    return APIKeyResponse(
        data={"key": key, "created_at": now},
        timestamp=now,
    )
