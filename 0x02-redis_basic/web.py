#!/usr/bin/env python3


import requests
import redis
import time
from functools import wraps

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_page(expiration: int):
    """
    A decorator to cache the page content and count accesses.

    Args:
        expiration (int): Time in seconds for the cache to expire.

    Returns:
        function: The wrapped function with caching and access counting.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url: str) -> str:
            # Increment the access count
            r.incr(f"count:{url}")

            cached_data = r.get(url)
            if cached_data:
                return cached_data.decode('utf-8')

            result = func(url)
            r.setex(url, expiration, result)

            return result

        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a given URL.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
