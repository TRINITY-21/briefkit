# Briefkit

REST API that serves weather, crypto, and news data with API key auth, rate limiting, and auto-generated Swagger docs.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/keys` | Generate a new API key |
| `GET` | `/api/weather/{city}` | Weather data for a city |
| `GET` | `/api/crypto/{coins}` | Crypto prices (comma-separated) |
| `GET` | `/api/news?limit=5` | Top Hacker News stories |
| `GET` | `/api/briefing` | Combined: weather + crypto + news |
| `GET` | `/docs` | Interactive Swagger UI |

## Auth

All endpoints except `/api/keys` and `/docs` require an API key:

```bash
# Generate a key
curl -X POST http://localhost:8000/api/keys

# Use it
curl -H "X-API-Key: bk_your_key" http://localhost:8000/api/weather/Istanbul
```

Rate limit: 100 requests/day per key.

## Response Format

```json
{
  "status": "ok",
  "data": { ... },
  "timestamp": "2026-01-01T00:00:00Z"
}
```

## APIs

| Source | Data |
|--------|------|
| [OpenWeatherMap](https://openweathermap.org/) | Weather: temp, humidity, wind, feels like |
| [CoinGecko](https://www.coingecko.com/) | Crypto: prices, 24h change, market cap |
| [Hacker News](https://news.ycombinator.com/) | News: top stories with scores and links |

## Stack

- **FastAPI** — auto-generated Swagger docs, Pydantic models
- **httpx** — async HTTP client for upstream APIs
- **SQLite / PostgreSQL** — API key storage
- **slowapi** — per-key rate limiting
- **In-memory TTL cache** — don't hammer upstream APIs

## Setup

```bash
git clone https://github.com/TRINITY-21/briefkit.git
cd briefkit
pip install -r requirements.txt
```

Create `.env`:

```
OPENWEATHER_API_KEY=your_key_here
DEFAULT_CITY=Istanbul
CRYPTO_COINS=bitcoin,ethereum,solana
DATABASE_URL=sqlite+aiosqlite:///./briefkit.db
```

Run:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API docs.

## Architecture

```
briefkit/
├── app/
│   ├── main.py          # FastAPI app, CORS, rate limiter, error handlers
│   ├── config.py         # pydantic-settings from .env
│   ├── database.py       # Async DB connection + api_keys table
│   ├── auth.py           # API key generation + verification dependency
│   ├── cache.py          # TTL cache decorator (in-memory)
│   ├── models.py         # Pydantic response models (auto Swagger schemas)
│   ├── routes/           # Endpoint handlers
│   └── services/         # Upstream API fetchers (weather, crypto, news)
├── Procfile              # Railway deployment
└── requirements.txt
```

**Key design decisions:**

- Services and routes are separate — services fetch data, routes handle HTTP
- Pydantic models define response shapes — Swagger docs auto-generated
- TTL cache prevents hammering upstream APIs (5min weather/news, 2min crypto)
- API keys prefixed with `bk_` for easy identification
- `asyncio.gather` for parallel fetches in `/briefing`

## License

MIT
