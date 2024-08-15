import requests
import time
from cachetools import TTLCache, cached
from functools import wraps

# Create a cache with a Time-To-Live (TTL) of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)
access_count = {}

# Decorator for caching and tracking
def cache_and_track(func):
    @wraps(func)
    def wrapper(url):
        # Track the number of accesses
        count_key = f"count:{url}"
        if count_key in access_count:
            access_count[count_key] += 1
        else:
            access_count[count_key] = 1
        
        # Check cache first
        if url in cache:
            return cache[url]
        
        # If not in cache, fetch the content
        result = func(url)
        cache[url] = result
        return result
    
    return wrapper

@cache_and_track
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://example.com"
    
    # First request, should fetch and cache the result
    print(get_page(url))
    
    # Wait for less than 10 seconds and fetch again, should return cached result
    time.sleep(5)
    print(get_page(url))
    
    # Wait for more than 10 seconds, cache should expire, and a new request should be made
    time.sleep(11)
    print(get_page(url))
    
    # Access count should reflect the number of times the URL was accessed
    print(f"Access count for {url}: {access_count[f'count:{url}']}")

