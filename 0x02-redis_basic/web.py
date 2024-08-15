#!/usr/bin/env python3

import requests
import time
from functools import wraps

# Dictionary to store cached data and access counts
cache = {}
access_count = {}

# Decorator for caching and counting accesses
def cache_page(expiration: int):
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            # Track the number of times the URL was accessed
            if f"count:{url}" not in access_count:
                access_count[f"count:{url}"] = 0
            access_count[f"count:{url}"] += 1

            # Check if the URL is in the cache and hasn't expired
            if url in cache:
                cached_data, timestamp = cache[url]
                if time.time() - timestamp < expiration:
                    return cached_data

            # Fetch new content, cache it, and return it
            result = func(url)
            cache[url] = (result, time.time())
            return result

        return wrapper
    return decorator

@cache_page(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
