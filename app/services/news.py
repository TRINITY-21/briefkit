import asyncio
import httpx
from app.cache import ttl_cache


async def _fetch_story(client: httpx.AsyncClient, story_id: int) -> dict | None:
    r = await client.get(
        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    )
    if r.status_code != 200:
        return None
    return r.json()


@ttl_cache(seconds=300)
async def fetch_news(limit: int = 5) -> list[dict] | None:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json"
        )
        if r.status_code != 200:
            return None
        ids = r.json()

        tasks = [_fetch_story(client, sid) for sid in ids[:limit]]
        items = await asyncio.gather(*tasks)

    stories = []
    for item in items:
        if item and item.get("title"):
            stories.append({
                "title": item["title"],
                "url": item.get("url", f"https://news.ycombinator.com/item?id={item['id']}"),
                "score": item.get("score", 0),
                "by": item.get("by", ""),
                "comments": item.get("descendants", 0),
            })
    return stories
