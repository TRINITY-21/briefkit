from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.auth import verify_api_key
from app.config import settings
from app.models import WeatherResponse, ErrorResponse
from app.services.weather import fetch_weather

router = APIRouter(prefix="/api", tags=["Weather"])


@router.get(
    "/weather/{city}",
    response_model=WeatherResponse,
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_weather(city: str, _key: str = Depends(verify_api_key)):
    if not settings.openweather_api_key:
        raise HTTPException(status_code=500, detail="Weather API not configured")

    data = await fetch_weather(city, settings.openweather_api_key)
    if not data:
        raise HTTPException(status_code=404, detail=f"Could not fetch weather for '{city}'")

    return WeatherResponse(data=data, timestamp=datetime.now(timezone.utc))
