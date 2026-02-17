<div align="center">

# Briefkit

**Weather, crypto, and news in one API call.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-Deployed-A855F7?style=flat-square&logo=railway&logoColor=white)

REST API with API key auth, rate limiting, TTL caching, and auto-generated Swagger docs.

[Live API](https://web-production-59874.up.railway.app) · [Swagger Docs](https://web-production-59874.up.railway.app/docs) · [Source Code](https://github.com/TRINITY-21/briefkit)

</div>

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/keys` | Generate a new API key |
| `GET` | `/api/weather/{city}` | Weather data for any city |
| `GET` | `/api/crypto/{coins}` | Crypto prices (comma-separated) |
| `GET` | `/api/news?limit=5` | Top Hacker News stories |
| `GET` | `/api/briefing` | Combined: weather + crypto + news |
| `GET` | `/docs` | Interactive Swagger UI |

## Quick Start

```bash
# 1. Get your API key
curl -X POST https://web-production-59874.up.railway.app/api/keys

# 2. Use it
curl -H "X-API-Key: bk_your_key" \
  https://web-production-59874.up.railway.app/api/briefing?city=Istanbul
```

## Response

```json
{
  "status": "ok",
  "data": {
    "weather": {
      "city": "Istanbul",
      "temp": 12.5,
      "feels_like": 10.2,
      "humidity": 65,
      "description": "partly cloudy",
      "wind_speed": 3.6
    },
    "crypto": [
      { "symbol": "BTC", "price": 67321.0, "change_24h": -0.28, "market_cap": 1344758503096 }
    ],
    "news": [
      { "title": "Show HN: ...", "url": "https://...", "score": 342, "comments": 89 }
    ]
  },
  "timestamp": "2026-02-17T16:00:00Z"
}
```

## Auth & Rate Limiting

- Pass your key via `X-API-Key` header
- 100 requests/day per key
- Keys prefixed with `bk_` for easy identification
- `/api/keys` and `/docs` are public (no auth needed)

## Data Sources

| Source | Data |
|--------|------|
| [OpenWeatherMap](https://openweathermap.org/) | Temperature, humidity, wind, conditions |
| [CoinGecko](https://www.coingecko.com/) | Prices, 24h change, market cap |
| [Hacker News](https://news.ycombinator.com/) | Top stories with scores and links |

## Stack

| Layer | Tech |
|-------|------|
| Framework | FastAPI with auto Swagger docs |
| HTTP Client | httpx (async) |
| Database | PostgreSQL (Railway) / SQLite (local) |
| Rate Limiting | slowapi (per-key) |
| Caching | In-memory TTL (5min weather, 2min crypto) |
| Models | Pydantic v2 (typed responses) |
| Deploy | Railway with Procfile |

## Local Development

```bash
git clone https://github.com/TRINITY-21/briefkit.git
cd briefkit
pip install -r requirements.txt
cp .env.example .env  # add your OpenWeatherMap key
uvicorn app.main:app --reload
```

## Architecture

```
briefkit/
├── app/
│   ├── main.py          # App setup, CORS, rate limiter, error handlers
│   ├── config.py         # pydantic-settings from .env
│   ├── database.py       # Async DB + api_keys table
│   ├── auth.py           # Key generation + verification dependency
│   ├── cache.py          # TTL cache decorator
│   ├── models.py         # Pydantic response schemas
│   ├── routes/           # weather, crypto, news, briefing, keys
│   ├── services/         # Upstream API fetchers
│   └── static/           # Custom landing page
├── Procfile              # Railway: uvicorn start command
└── requirements.txt
```

**Design decisions:**
- Services and routes are separate — services have no HTTP framework imports
- `/briefing` fetches all 3 sources in parallel via `asyncio.gather`
- TTL cache avoids hammering upstream APIs on repeated requests
- Pydantic models auto-generate Swagger JSON schemas

## License

MIT
