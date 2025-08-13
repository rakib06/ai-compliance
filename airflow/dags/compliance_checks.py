from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os

# Make backend importable if mounted at /opt/app
import sys
if "/opt/app" not in sys.path:
    sys.path.append("/opt/app")

from backend.db import SessionLocal
from backend.jobs.batch_checks import run_scheduled_checks

def _run_checks():
    with SessionLocal() as s:
        flagged = run_scheduled_checks(s)
        print(f"Flagged: {flagged}")
        return flagged

with DAG(
    dag_id="compliance_scheduled_checks",
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args={"retries": 0},
    tags=["compliance"],
) as dag:
    run = PythonOperator(task_id="run_checks", python_callable=_run_checks)
