#!/bin/bash
set -e

# Wait for Postgres for relevant services
if [ "$SERVICE_TYPE" != "postgres" ]; then
  wait-for-it.sh postgres:5432 --timeout=60 -- echo "PostgreSQL is ready"
fi

case "$SERVICE_TYPE" in
  airflow-webserver)
    echo "Running migrations and creating admin user..."
    airflow db migrate

    airflow users create \
      --username admin \
      --firstname Satya \
      --lastname Admin \
      --role Admin \
      --email muddalasatyanarayana96@gmail.com \
      --password admin123 || echo "User may already exist. Skipping."

    exec airflow webserver
    ;;
  airflow-scheduler)
    exec airflow scheduler
    ;;
  flask)
    exec python src/api/app.py
    ;;
  mlflow)
    exec mlflow ui \
      --host 0.0.0.0 \
      --port 5001 \
      --backend-store-uri postgresql+psycopg2://${ML_USER}:${ML_PASSWORD}@postgres:5432/${ML_NAME} \
      --default-artifact-root /app/mlruns \
      --gunicorn-opts "--log-level debug"
    ;;
  *)
    echo "Unknown service type: $SERVICE_TYPE"
    exit 1
    ;;
esac
