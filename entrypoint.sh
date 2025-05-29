#!/bin/sh
set -eu

# Wait for PostgreSQL to be ready
wait-for-it.sh "${DB_HOST:-postgres}:${DB_PORT:-5432}" -t 30

# Run the appropriate service based on SERVICE_TYPE
case "$SERVICE_TYPE" in
  "flask")
    echo "Starting Flask application..."
    exec python -m src.main
    ;;
  "airflow-webserver")
    echo "Starting Airflow webserver..."
    # Run migrations and create admin user
    airflow db upgrade
    airflow users create \
      --username admin \
      --firstname Satya \
      --lastname Admin \
      --role Admin \
      --email muddalasatyanarayana96@gmail.com \
      --password admin123 \
    || echo "Admin user already exists or creation failed, continuing..."
    exec airflow webserver
    ;;
  "airflow-scheduler")
    echo "Starting Airflow scheduler..."
    airflow db upgrade
    exec airflow scheduler
    ;;
  *)
    echo "Unknown SERVICE_TYPE: $SERVICE_TYPE"
    exit 1
    ;;
esac
