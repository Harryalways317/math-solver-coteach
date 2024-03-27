import asyncio
from functools import wraps
import diskcache as dc

cache = dc.Cache('./.cache')
def cache_response(timeout: int = 8640000):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            result = cache.get(cache_key)
            # print(f"Cache key {cache_key} result {result}")
            if result is None:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    print('cache hit')
                    result = func(*args, **kwargs)
                cache.set(cache_key, result, expire=timeout)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            result = cache.get(cache_key)
            # print(f"Cache key {cache_key} result {result}")
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, expire=timeout)
            else:
                print('cache hit')
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
