from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.database import database
from app.routes import weather, crypto, news, briefing, keys


def _get_api_key(request: Request):
    return request.headers.get("X-API-Key", get_remote_address(request))


limiter = Limiter(key_func=_get_api_key)

app = FastAPI(
    title="Briefkit",
    description="Weather, crypto, and news API with API key auth and rate limiting.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "detail": "Rate limit exceeded. 100 requests/day per API key.",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(keys.router)
app.include_router(weather.router)
app.include_router(crypto.router)
app.include_router(news.router)
app.include_router(briefing.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
