# 📈 Crypto Price Prediction

A complete end-to-end machine learning and MLOps project to predict cryptocurrency prices using a modular, production-grade pipeline. This project combines data ingestion, ETL processing, machine learning, monitoring, and a Flask-based web application. It supports both local development and Docker-based deployment with Airflow, MLflow, and GitHub Actions.

---

## 🚀 Features

- 🧪 ML pipeline for training and evaluation
- 🔄 ETL pipeline with Airflow DAGs
- 🧠 Model monitoring and drift detection
- 🌐 Flask web API for live predictions
- 📊 MLflow for model tracking
- 📦 Docker + Docker Compose for full environment setup
- 📝 CI/CD pipeline with GitHub Actions
- 🛠️ Centralized logging and config management
- 💾 PostgreSQL database for structured data storage

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
├── pipeline_config.yaml  # YAML config for pipeline and DAGs
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup file
├── .env                  # Environment variables
├── .gitignore            # Git ignore rules
├── .dockerignore         # Docker ignore rules
└── README.md             # You're reading it!

🧰 Setup Instructions

✅ 1. Clone the Repository
git clone https://github.com/<your-username>/crypto-price-prediction.git
cd crypto-price-prediction

🐍 2. Create Conda Environment
conda create -n crypto python=3.10
conda activate crypto

📦 3. Install Dependencies
pip install -r requirements.txt
pip install -e .
setup.py enables simple module-level imports like:

⚙️ 4. Configuration
.env: Stores environment secrets (API keys, DB credentials)
pipeline_config.yaml: Config for DAGs, file paths, and run settings
config.py: Python classes for global config management

🐳 Docker Usage
🔁 Option 1: Pull Image from DockerHub
docker pull <your-dockerhub-username>/crypto-price-prediction:latest
docker-compose up --build

🧪 Option 2: Build Locally
docker build -t crypto-price-prediction .
docker run -p 5000:5000 crypto-price-prediction

⚠️ Docker Volumes
Make sure Docker volumes are mapped for:
Airflow DAGs
Data and logs
pipeline_config.yaml

🐘 PostgreSQL in Docker
Export CSV from DB:
docker exec -it pg_container bash
su - postgres
psql
\c crypto_db
COPY transactions TO '/tmp/transactions.csv' WITH CSV HEADER;
exit
docker cp pg_container:/tmp/transactions.csv ./transactions.csv

🌐 Run Locally Without Docker
conda activate crypto
python src/web/main.py

🛫 Airflow Quickstart (With Docker)
docker-compose -f docker-compose.airflow.yml up --build
Access: http://localhost:8080
Username/Password: airflow
Ensure proper volume mapping for dags/ and configs.

📊 MLflow Usage
mlflow ui --backend-store-uri ./mlruns
Access at: http://localhost:5000
Tracks: models, parameters, metrics, artifacts

🧠 Model Flow
graph TD
main.py --> app.py --> routes.py --> model_service.py & data_service.py

🛠️ Airflow DAGs
etl_pipeline.py	    - Automates data ingestion
model_pipeline.py   - Trains and evaluates models
monitor_pipeline.py - Checks model performance & drift

All DAGs are scheduled and triggered via Airflow and configured using pipeline_config.yaml.

🔄 GitHub Actions (CI/CD)
Configured workflows in .github/workflows/ci-cd.yml include:
✅ Code linting with flake8
✅ Unit tests with pytest
✅ Docker build and push to DockerHub
✅ (Optional) Deployment to production server

🔬 Testing
Run tests locally using:
pytest tests/
Covers ETL, model, web, and config modules.

🧠 Best Practices Followed
🔹 Modular codebase with reusable components
🔹 Secrets and configs abstracted via .env and config.py
🔹 Centralized logging for debugging and observability
🔹 Fully containerized setup using Docker and Docker Compose
🔹 DAG-driven automation with Apache Airflow
🔹 Model lifecycle tracking via MLflow
🔹 Automated CI/CD with GitHub Actions
🔹 PostgreSQL as persistent data backend

🧑‍💻 Contributing
Contributions are welcome!
Fork the repository
Create a feature branch
Commit and push your changes
Open a pull request

📄 License
This project is licensed under the MIT License.

📬 Contact
Maintainer: satyanarayana
Email: msatya8055@gmail.com
GitHub: satyanarayana8055
