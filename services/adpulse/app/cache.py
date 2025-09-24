import os
import redis

REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/1")
r = redis.from_url(REDIS_URL, decode_responses=True)

def cache_get(key: str):
    return r.get(key)

def cache_set(key: str, val: str, ttl=30):
    r.setex(key, ttl, val)