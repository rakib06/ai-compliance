
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import select
from backend import config
from backend.db import SessionLocal, init_db
from backend.models.entities import Document, Entity, Transaction, CaseFlag
from backend.pipeline.ocr import ocr_bytes
from backend.pipeline.ner import extract_entities

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": config.ALLOWED_ORIGINS}})

@app.route("/api/health", methods=["GET"])
def health():
    return {"ok": True}

@app.route("/api/upload_doc", methods=["POST"])
def upload_doc():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "no file"}), 400
    data = file.read()
    text = ocr_bytes(data, file.filename)
    with SessionLocal() as s:
        doc = Document(filename=file.filename, content=text)
        s.add(doc)
        s.flush()
        ents = extract_entities(text)
        for label, etxt in ents:
            s.add(Entity(doc_id=doc.id, label=label, text=etxt[:255]))
        s.commit()
        return jsonify({"doc_id": doc.id, "entities": [{"label": l, "text": t} for l,t in ents]})

@app.route("/api/transactions/ingest", methods=["POST"])
def ingest_transactions():
    payload = request.get_json(force=True)
    rows = payload if isinstance(payload, list) else payload.get("rows", [])
    created = 0
    with SessionLocal() as s:
        for r in rows:
            tx = Transaction(
                customer_id=str(r.get("customer_id","")),
                amount=float(r.get("amount",0)),
                currency=r.get("currency","USD"),
                country=r.get("country",""),
                description=r.get("description",""),
            )
            s.add(tx); created += 1
        s.commit()
    return {"created": created}

@app.route("/api/cases", methods=["GET"])
def list_cases():
    with SessionLocal() as s:
        q = s.execute(select(CaseFlag, Transaction).join(Transaction, CaseFlag.transaction_id==Transaction.id)).all()
        out = []
        for flag, tx in q:
            out.append({
                "case_id": flag.id, "tx_id": tx.id, "customer_id": tx.customer_id,
                "amount": tx.amount, "currency": tx.currency, "country": tx.country,
                "description": tx.description, "reason": flag.reason, "semantic_score": flag.semantic_score
            })
        return {"cases": out}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)
