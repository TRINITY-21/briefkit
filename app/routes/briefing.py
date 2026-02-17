import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query

from app.auth import verify_api_key
from app.config import settings
from app.models import BriefingResponse, BriefingData
from app.services.weather import fetch_weather
from app.services.crypto import fetch_crypto
from app.services.news import fetch_news

router = APIRouter(prefix="/api", tags=["Briefing"])


async def _none():
    return None


@router.get("/briefing", response_model=BriefingResponse)
async def get_briefing(
    city: str = Query(default=None),
    coins: str = Query(default=None),
    limit: int = Query(default=5, ge=1, le=30),
    _key: str = Depends(verify_api_key),
):
    city = city or settings.default_city
    coin_tuple = tuple(
        c.strip().lower() for c in (coins or settings.crypto_coins).split(",")
    )

    weather, crypto, news = await asyncio.gather(
        fetch_weather(city, settings.openweather_api_key)
        if settings.openweather_api_key
        else _none(),
        fetch_crypto(coin_tuple),
        fetch_news(limit=limit),
    )

    return BriefingResponse(
        data=BriefingData(
            weather=weather,
            crypto=crypto or [],
            news=news or [],
        ),
        timestamp=datetime.now(timezone.utc),
    )
