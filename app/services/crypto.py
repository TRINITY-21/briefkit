import httpx
from app.cache import ttl_cache

SYMBOL_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "dogecoin": "DOGE",
    "cardano": "ADA",
    "polkadot": "DOT",
    "ripple": "XRP",
}


@ttl_cache(seconds=120)
async def fetch_crypto(coins: tuple) -> list[dict] | None:
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.coingecko.com/api/v3/simple/price", params=params
        )
        if r.status_code != 200:
            return None
        data = r.json()

    results = []
    for coin_id in coins:
        if coin_id in data:
            coin = data[coin_id]
            sym = SYMBOL_MAP.get(coin_id, coin_id.upper()[:4])
            results.append({
                "symbol": sym,
                "price": coin.get("usd", 0),
                "change_24h": coin.get("usd_24h_change", 0),
                "market_cap": coin.get("usd_market_cap", 0),
            })
    return results
