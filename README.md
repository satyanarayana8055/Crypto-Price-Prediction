# 📈 Crypto Price Prediction

A complete end-to-end machine learning and MLOps project to predict cryptocurrency prices using a modular, production-grade pipeline. This project combines data ingestion, ETL processing, machine learning, monitoring, and a Flask-based web application. It supports both local development and Docker-based deployment with Airflow integration.

---

## 🚀 Features

- 🧪 ML pipeline for training and evaluation
- 🔄 ETL pipeline with Airflow DAGs
- 🧠 Model monitoring and drift detection
- 🌐 Flask web API for live predictions
- 📦 Docker + Docker Compose for full environment setup
- 📝 CI/CD pipeline with GitHub Actions
- 🛠️ Centralized logging and config management

---

## 🧱 Project Structure

```bash
project-root/
│
├── .github/              # GitHub Actions CI/CD setup
├── dags/                 # Airflow DAGs for ETL, training, and monitoring
├── data/                 # Raw, processed, and model storage
├── notebook/             # Jupyter notebooks (EDA, experiments)
├── src/                  # All source code (web, services, ML, monitoring)
│   ├── web/              # Flask web app and API
│   ├── services/         # Business logic for model and data
│   ├── config/           # Configuration classes and environment
│   ├── etl/              # ETL pipeline scripts (extract, transform, load)
│   ├── ml_components/    # Preprocessing, training, feature engineering
│   ├── monitoring/       # Drift detection, performance monitoring
│   └── utils/            # Logger and helper functions
├── logs/                 # Logs for ETL, app, and model
├── tests/                # Unit tests for different components
├── Dockerfile            # Docker setup for the app
├── docker-compose.yml    # Multi-service Docker orchestration
├── .env                  # Environment variables
├── .gitignore            # Git ignore rules
├── .dockerignore         # Docker ignore rules
├── Makefile              # Predefined shell commands
├── pipeline_config.yaml  # YAML config for pipeline and DAGs
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Optional project build metadata
└── README.md             # You're reading it!
