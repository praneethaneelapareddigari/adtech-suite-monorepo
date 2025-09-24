import os, asyncio
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends
from sqlalchemy import text
from .db import engine, init
from .kafka_io import publish, close as kafka_close
from .cache import cache_get, cache_set

app = FastAPI(title="AdPulse++ — Real-Time Ad Analytics API")

class EventIn(BaseModel):
    event_id: str
    campaign_id: str
    user_id: str
    timestamp: datetime = Field(alias="timestamp")
    action: str
    bid_price: float

@app.on_event("startup")
def on_start():
    init()

@app.on_event("shutdown")
async def on_stop():
    await kafka_close()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/events")
async def ingest(e: EventIn):
    # store minimal to Postgres
    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO ad_events(event_id, campaign_id, user_id, ts, action, bid_price)
        VALUES (:event_id, :campaign_id, :user_id, :ts, :action, :bid_price)
        ON CONFLICT (event_id) DO NOTHING
        """), dict(event_id=e.event_id, campaign_id=e.campaign_id, user_id=e.user_id,
                     ts=e.timestamp, action=e.action, bid_price=e.bid_price))
    # publish to Kafka for downstream consumers
    await publish(e.model_dump(by_alias=True))
    return {"status": "queued"}

@app.get("/reports")
def reports(campaign_id: str):
    key = f"rep:{campaign_id}"
    cached = cache_get(key)
    if cached:
        return {"cached": True, "data": eval(cached)}
    with engine.begin() as conn:
        rows = conn.execute(text("""
        SELECT action, count(*) AS cnt
        FROM ad_events WHERE campaign_id=:cid GROUP BY action
        """), {"cid": campaign_id}).mappings().all()
    data = {r["action"]: int(r["cnt"]) for r in rows}
    cache_set(key, repr(data), ttl=30)
    return {"cached": False, "data": data}