# Airflow notes

This dev setup expects the repo mounted at **/opt/app** inside the Airflow container
so the DAG can import backend code. If using Docker Compose provided here,
that mount is already configured.

DAG: `compliance_scheduled_checks` runs hourly by default.
