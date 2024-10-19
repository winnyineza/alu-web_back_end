#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests

# Initialize Redis connection
r = redis.Redis()

def get_page(url: str) -> str:
    """ Track how many times a particular URL was accessed in the key
        "count:{url}" and cache the result with an expiration time of 10 seconds """
    
    # Increment the access count for the URL
    r.incr(f"count:{url}")
    
    # Check if the URL is already cached
    cached_response = r.get(f"cached:{url}")

    if cached_response:
        # Return the cached response if it exists
        return cached_response.decode('utf-8')

    # If not cached, fetch the page
    resp = requests.get(url)

    # Cache the response with an expiration time of 10 seconds
    r.setex(f"cached:{url}", 10, resp.text)

    return resp.text

if __name__ == "__main__":
    # Test the function with the provided URL
    print(get_page('http://slowwly.robertomurray.co.uk/delay/10/url/http://example.com'))
