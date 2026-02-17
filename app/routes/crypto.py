from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.auth import verify_api_key
from app.models import CryptoResponse, ErrorResponse
from app.services.crypto import fetch_crypto

router = APIRouter(prefix="/api", tags=["Crypto"])


@router.get(
    "/crypto/{coins}",
    response_model=CryptoResponse,
    responses={401: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
)
async def get_crypto(coins: str, _key: str = Depends(verify_api_key)):
    coin_list = tuple(c.strip().lower() for c in coins.split(","))

    data = await fetch_crypto(coin_list)
    if not data:
        raise HTTPException(status_code=502, detail="Could not fetch crypto prices")

    return CryptoResponse(data=data, timestamp=datetime.now(timezone.utc))
