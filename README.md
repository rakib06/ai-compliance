# AI-Powered Compliance Workflow Automation (Starter)

This repo is a **batteries-included scaffold** for a mock compliance pipeline (KYC OCR + NER + FAISS + rule/semantic flagging) with:
- **Backend:** Flask + SQLAlchemy + FAISS + spaCy/HF + OpenAI Embeddings
- **Frontend:** React + TypeScript (Vite) for uploads and case monitoring
- **Automation:** Apache Airflow DAG that periodically scores new transactions
- **PostgreSQL** for storage

> ⚠️ This is a **mock/demo** system — not production compliance software.

## Quick Start (Dev, no Docker)

1. **Environment**
   ```bash
   python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
   pip install -r backend/requirements.txt
   cp .env.example .env
   # edit .env with your keys
   ```

2. **Run Postgres** (docker or local). With docker:
   ```bash
   docker run --name comp-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
   ```

3. **DB init & dev server**
   ```bash
   python backend/db.py --init
   python backend/app.py
   ```

4. **Frontend**
   ```bash
   cd frontend
   npm i
   npm run dev
   ```

5. **Airflow (optional quick dev)**
   - Install Airflow locally, or run the **Docker Compose** service (see below).
   - Put your DB URL into Airflow env `PROJECT_DATABASE_URL` (see `.env.example`).
   - The example DAG lives in `airflow/dags/compliance_checks.py`.

## Docker Compose (Dev all-in-one)

> This is a lightweight dev setup. It uses Airflow `standalone` for convenience.

```bash
cp .env.example .env
docker compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Airflow UI: http://localhost:8080 (user/pass printed on first run)
- Postgres: localhost:5432 (user: postgres / pass: postgres)

## What’s Included

- **OCR** via Tesseract (or swap to AWS Textract)
- **NER** via spaCy (en_core_web_sm by default)
- **Embeddings** via OpenAI (text-embedding-3-*)
- **FAISS** vector index for pattern/typology similarity
- **Rule-based** checks + **semantic** similarity scoring
- **Airflow DAG** to batch-score new transactions hourly

## Project Structure

```
backend/
  app.py              # Flask API: upload, ingest transactions, list cases
  config.py           # env config
  db.py               # SQLAlchemy engine + Base + init
  models/             # ORM models
  pipeline/           # OCR, NER, embeddings, FAISS
  detection/          # rules + semantic scorer
  jobs/               # batch scoring callable (used by Airflow)
airflow/
  dags/compliance_checks.py
frontend/
  src/ (Upload / Cases UI)
docs/
  architecture.md
docker-compose.yml
```

## Next Steps

- Swap to AWS Textract in `pipeline/ocr.py` if desired.
- Tune rules in `detection/rules.py` and typology phrases in `detection/scorer.py`.
- Add authentication, audit logs, and PII handling per your org’s policy.
- Write unit tests (pytest) for pipelines and rules.
