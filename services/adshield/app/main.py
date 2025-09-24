from fastapi import FastAPI
from pydantic import BaseModel
from .rules import rules_score, rule_ip_reputation
from .model import ToyFraudModel
from .cache import incr_counter, get_counter

app = FastAPI(title="AdShield++ — Fraud Scoring API")
MODEL = ToyFraudModel()

class ScoreIn(BaseModel):
    event_id: str
    ip: str
    user_id: str
    ua: str | None = None
    bid_price: float
    ts: str

@app.get("/health")
def health():
    return {"ok": True, "scored": get_counter("scored")}

@app.post("/score")
def score(body: ScoreIn):
    rules = rules_score(body.ip, body.bid_price, body.ua or "")
    proba = MODEL.predict_proba(bid=body.bid_price, ip_bad=int(rule_ip_reputation(body.ip)>0))
    risk = min(1.0, 0.15*rules + 0.85*proba)
    incr_counter("scored")
    return {"event_id": body.event_id, "risk": round(risk, 4), "decision": "BLOCK" if risk>0.7 else "ALLOW",
            "explain": {"rules": rules, "ml_proba": round(proba,4)}}