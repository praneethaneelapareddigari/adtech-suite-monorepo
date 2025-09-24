import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://adtech:adtechpass@postgres:5432/adtech")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ad_events (
          event_id TEXT PRIMARY KEY,
          campaign_id TEXT,
          user_id TEXT,
          ts TIMESTAMP,
          action TEXT,
          bid_price NUMERIC
        );
        """))
        conn.execute(text("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS campaign_stats AS
        SELECT campaign_id, action, count(*) AS cnt
        FROM ad_events GROUP BY campaign_id, action;
        """))