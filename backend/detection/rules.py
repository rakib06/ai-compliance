from typing import Dict, List

HIGH_RISK_COUNTRIES = {"IR", "KP", "SY"}  # demo only
AMOUNT_THRESHOLD = 10000.0

def apply_rules(tx: Dict) -> List[str]:
    hits = []
    if tx.get("amount", 0) >= AMOUNT_THRESHOLD:
        hits.append("R1_HIGH_AMOUNT")
    if tx.get("country") in HIGH_RISK_COUNTRIES:
        hits.append("R2_HIGH_RISK_COUNTRY")
    if "cash" in (tx.get("description","").lower()):
        hits.append("R3_CASH_REFERENCE")
    return hits
