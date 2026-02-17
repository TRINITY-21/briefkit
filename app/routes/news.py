from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import verify_api_key
from app.models import NewsResponse, ErrorResponse
from app.services.news import fetch_news

router = APIRouter(prefix="/api", tags=["News"])


@router.get(
    "/news",
    response_model=NewsResponse,
    responses={401: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
)
async def get_news(
    limit: int = Query(default=5, ge=1, le=30),
    _key: str = Depends(verify_api_key),
):
    data = await fetch_news(limit=limit)
    if not data:
        raise HTTPException(status_code=502, detail="Could not fetch news")

    return NewsResponse(data=data, timestamp=datetime.now(timezone.utc))
