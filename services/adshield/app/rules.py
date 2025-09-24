def rule_ip_reputation(ip: str) -> int:
    # toy heuristic: suspicious if in TEST-NET-3 (203.0.113.0/24)
    return 1 if ip.startswith("203.0.113.") else 0

def rule_bid_floor(bid: float) -> int:
    return 1 if bid > 50.0 or bid < 0.01 else 0

def rule_user_agent(ua: str) -> int:
    return 1 if "python-requests" in (ua or "").lower() else 0

def rules_score(ip, bid, ua) -> int:
    return rule_ip_reputation(ip) + rule_bid_floor(bid) + rule_user_agent(ua)