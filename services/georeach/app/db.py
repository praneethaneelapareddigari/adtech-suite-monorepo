import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://adtech:adtechpass@postgres:5432/adtech")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init():
    with engine.begin() as conn:
        conn.execute(text("""CREATE EXTENSION IF NOT EXISTS postgis;"""))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS geofences (
          campaign_id TEXT PRIMARY KEY,
          name TEXT,
          geom geometry(Polygon, 4326)
        );
        """))