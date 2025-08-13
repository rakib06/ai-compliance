from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.entities import Transaction, CaseFlag
from backend.detection.rules import apply_rules
from backend.detection.scorer import semantic_score

def run_scheduled_checks(session: Session, semantic_threshold: float = 0.35) -> int:
    """Score unscored transactions; return number flagged."""
    txs = session.execute(select(Transaction).where(Transaction.scored == False)).scalars().all()  # noqa: E712
    flagged = 0
    for tx in txs:
        rules = apply_rules({
            "amount": tx.amount, "country": tx.country, "description": tx.description
        })
        best_id, score, phrase = semantic_score(tx.description or "")
        reason_parts = []
        if rules:
            reason_parts.append(f"rules={','.join(rules)}")
        if score >= semantic_threshold:
            reason_parts.append(f"semantic_match='{phrase}' ({score:.2f})")
        if reason_parts:
            flag = CaseFlag(transaction_id=tx.id, rule_hits=",".join(rules), semantic_score=score, reason="; ".join(reason_parts))
            session.add(flag)
            flagged += 1
        tx.scored = True
    session.commit()
    return flagged
