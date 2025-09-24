from fastapi import FastAPI, Query
from sqlalchemy import text
from shapely.geometry import Polygon, Point
from .db import engine, init
from .cache import cache_get, cache_set
from .models import CampaignIn

app = FastAPI(title="GeoReach++ — Geofencing API")

@app.on_event("startup")
def on_start():
    init()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/campaigns")
def create_campaign(body: CampaignIn):
    poly = Polygon(body.polygon)
    if not poly.is_valid:
        return {"error": "Invalid polygon"}
    wkt = poly.wkt  # WKT for PostGIS
    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO geofences(campaign_id, name, geom)
        VALUES (:cid, :name, ST_GeomFromText(:wkt, 4326))
        ON CONFLICT (campaign_id) DO UPDATE SET name=EXCLUDED.name, geom=EXCLUDED.geom
        """), dict(cid=body.campaign_id, name=body.name, wkt=wkt))
    return {"status": "upserted", "campaign_id": body.campaign_id}

@app.get("/hit")
def hit(lat: float = Query(...), lon: float = Query(...)):
    key = f"hit:{lat:.4f}:{lon:.4f}"
    c = cache_get(key)
    if c:
        return {"cached": True, "campaigns": c.split(',') if c else []}
    with engine.begin() as conn:
        rows = conn.execute(text("""
        SELECT campaign_id FROM geofences
        WHERE ST_Contains(geom, ST_SetSRID(ST_Point(:lon,:lat),4326))
        """), dict(lat=lat, lon=lon)).fetchall()
    cids = [r[0] for r in rows]
    cache_set(key, ",".join(cids), ttl=30)
    return {"cached": False, "campaigns": cids}