import os, redis
REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/3")
r = redis.from_url(REDIS_URL, decode_responses=True)

def incr_counter(k): return r.incr(k)
def get_counter(k): return int(r.get(k) or 0)