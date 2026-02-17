import time
from functools import wraps

_cache = {}


def ttl_cache(seconds: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in _cache:
                result, ts = _cache[key]
                if now - ts < seconds:
                    return result
            result = await func(*args, **kwargs)
            if result is not None:
                _cache[key] = (result, now)
            return result
        return wrapper
    return decorator
