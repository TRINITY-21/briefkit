from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ── Weather ──────────────────────────────────────────

class WeatherData(BaseModel):
    city: str
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    description: str
    wind_speed: float


class WeatherResponse(BaseModel):
    status: str = "ok"
    data: WeatherData
    timestamp: datetime


# ── Crypto ───────────────────────────────────────────

class CoinData(BaseModel):
    symbol: str
    price: float
    change_24h: float
    market_cap: float


class CryptoResponse(BaseModel):
    status: str = "ok"
    data: list[CoinData]
    timestamp: datetime


# ── News ─────────────────────────────────────────────

class StoryData(BaseModel):
    title: str
    url: str
    score: int
    by: str
    comments: int


class NewsResponse(BaseModel):
    status: str = "ok"
    data: list[StoryData]
    timestamp: datetime


# ── Briefing ─────────────────────────────────────────

class BriefingData(BaseModel):
    weather: Optional[WeatherData] = None
    crypto: list[CoinData] = []
    news: list[StoryData] = []


class BriefingResponse(BaseModel):
    status: str = "ok"
    data: BriefingData
    timestamp: datetime


# ── API Key ──────────────────────────────────────────

class APIKeyData(BaseModel):
    key: str
    created_at: datetime


class APIKeyResponse(BaseModel):
    status: str = "ok"
    data: APIKeyData
    timestamp: datetime


# ── Error ────────────────────────────────────────────

class ErrorResponse(BaseModel):
    status: str = "error"
    detail: str
    timestamp: datetime
