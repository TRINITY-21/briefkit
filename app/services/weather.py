import httpx
from app.cache import ttl_cache


@ttl_cache(seconds=300)
async def fetch_weather(city: str, api_key: str) -> dict | None:
    params = {"q": city, "appid": api_key, "units": "metric"}
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.openweathermap.org/data/2.5/weather", params=params
        )
        if r.status_code != 200:
            return None
        data = r.json()

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }
