# Architecture

```mermaid
flowchart LR
  subgraph Frontend [React/TS Dashboard]
    U[Upload KYC Docs] -->|/api/upload_doc| BAPI
    V[View Flagged Cases] -->|/api/cases| BAPI
  end

  subgraph Backend [Flask Service]
    BAPI[REST API]
    OCR[OCR (Tesseract/Textract)]
    NER[NER (spaCy/HF)]
    EMB[OpenAI Embeddings]
    VS[FAISS Index]
    RULES[Rule Engine]
    DB[(PostgreSQL)]
    JOBS[Batch Checks]
  end

  BAPI --> DB
  BAPI --> OCR --> NER --> DB
  BAPI --> EMB --> VS
  JOBS --> RULES --> DB
  JOBS --> EMB --> VS
  DB <---> VS

  subgraph Airflow [Scheduler]
    DAG[DAG: compliance_scheduled_checks]
  end
  DAG --> JOBS
```
