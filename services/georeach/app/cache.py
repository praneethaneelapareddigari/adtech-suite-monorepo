import os, redis
REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/2")
r = redis.from_url(REDIS_URL, decode_responses=True)

def cache_get(k): return r.get(k)
def cache_set(k,v,ttl=60): r.setex(k, ttl, v)