# Crypto-Price-Prediction

# This project stucture and pipeline for flow
project-root/
│
├── .github/                         # GitHub Actions CI/CD setup
│   └── workflows/
│       └── ci-cd.yml                # Defines CI/CD pipeline (e.g., test, build, deploy)
│
├── dags/                            # Airflow DAGs for automation
│   ├── etl_pipeline.py              # Automates ETL tasks
│   ├── model_pipeline.py            # Automates model training
│   └── monitor_pipeline.py          # Automates model monitoring
│
├── data/                            # Data storage folder
│   ├── raw/                         # Stores raw unprocessed data
│   ├── model/                       # Stores trained models
│   └── processed/                   # Stores clean, transformed data
│
├── Dockerfile                       # Containerizes app (web/API/ML)
├── docker-compose.yml               # Defines multi-container setup (API, Airflow, etc.)
│
├── notebook/                        # For Jupyter notebooks
│   └── EDA/
│       └── eda.ipynb                # Exploratory Data Analysis notebook
│
├── src/                             # Source code lives here
│   ├── web/                         # Web interface (Flask)
│   │   ├── api/                     # Web API (Flask app)
│   │   │   ├── __init__.py          # Initializes Flask API package
│   │   │   ├── app.py               # Flask app factory (creates app instance)
│   │   │   ├── routes.py            # Defines web routes/endpoints (e.g., /predict)
│   │   │   ├── static/              # Static files (CSS, JS)
│   │   │   │   ├── css/
│   │   │   │   └── js/
│   │   │   ├── templates/           # HTML templates for Flask (e.g., index.html)
│   │   ├── services/                # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── model_service.py     # Loads model and makes predictions
│   │   │   ├── notify_service.py    # Sends alerts/notifications
│   │   │   ├── data_service.py      # Fetches latest crypto data
│   │   │   └── exceptions.py        # Custom error handling
│   │   └── main.py                  # Entrypoint for web app
│
│   ├── config/                      # Configuration files
│   │   ├── __init__.p
│   │   ├── cyclelic_config.py       # this config avoids cyclic issue in logs and config files           
│   │   └── config.py                # Python config class for app (API keys, DB URL)
│
│   ├── etl/                         # ETL pipeline code
│   │   ├── __init__.py
│   │   ├── extract.py               # Pulls data from APIs
│   │   ├── transform.py             # Cleans and transforms data
│   │   └── load.py                  # Saves transformed data to file/db
│
│   ├── ml_components/               # ML pipeline code
│   │   ├── __init__.py
│   │   ├── ingestion.py             # Loads and splits data
│   │   ├── preprocessing.py         # Scaling, encoding, imputation
│   │   ├── extraction.py            # Technical indicators, time features
│   │   ├── model.py                 # Model training/saving/loading
│   │   └── evaluate.py              # Evaluation metrics (RMSE, accuracy)
│
│   ├── monitoring/                  # Model performance monitoring
│   │   ├── __init__.py
│   │   ├── drift_analysis.py        # Checks for data drift
│   │   └── performance_metrics.py   # Accuracy, loss monitoring
│
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py                # Logging setup
│   │   └── helper.py                # Helper functions (e.g., timestamp, formatting)
│
├── logs/                            # Logs generated from app/model/ETL
│   ├── etl.log
│   ├── app.log
│   └── model.log
│
├── tests/                           # Testing code
│   ├── test_data.py                 # Unit tests for ETL and data
│   ├── test_model.py                # Unit tests for model
│   └── test_app.py                  # Unit tests for web app/API
│
├── pipeline_config.yaml             # Configuration file for DAGs, Docker, ETL
├── .env                             # Environment variables (API keys, secrets)
├── .gitignore                       # Ignore folders/files from git
├── .dockerignore                    # Ignore folders/files from Docker build
├── Makefile                         # Useful commands (e.g., make train, make run)
├── README.md                        # Project overview/documentation
├── requirements.txt                 # Python dependencies
├── pyproject.Toml                   # Project metadata/setup (if using build system)
├── dvc.yaml

# setup instructions
1. Clone the Repository
git clone repo link
cd to repo name

2. Create conda envnirnment 
conda create -n crypto python=3.10

3. Install requirements.txt 
Create setup.py file it is used to import every required file as module. we no need to mention complete import module for example 
from src.scripts.data_ingestion import load_data
we can write like this 
from data_ingestion import load_data
pip install requirements.txt
pip install -e .

4. Set up config.py file for modular coding and avoid hard coding and it is like a controler we can change main parmas here 
pipeline_config.yaml is there for the pipeline line it human readable and userfor airflow and docker in any enviroment acceptable 

5. Set up logger file it is very import to mention loggers in every peice of because it is import to track the flow and where we get the error because of logs we can do the debuging easily

6. Create .env file for secure the Keys and Passwords

7. Set up gitigone file to ignore tracking of not need files and folders

8. Set Up PostgreSQL 
sudo -i -u postgres
psql
create user crypto_user with passsword '1234';
create database crypto_db;
create database airflow_db;
grant all privileges on database crypto_db, airflow_db to crypto_user;

9. but as real world project we no need to create any db in local system we have to crate docker images for every data storage 
how we can find the data in db first we have to execuite the image of the db 
docker exec -it 2a347fe51d75 bash
and then use the db crediential to login
psql -U crypto_user -d crypto_db
and fetch the data
from docker we can get the csv file with this commands
docker exec -it pg_container bash
su - postgres
psql
\c crypto_db
COPY transactions TO '/tmp/transactions.csv' WITH CSV HEADER;
docker cp pg_container:/tmp/transactions.csv ./transactions.csv

10. Airflow are are very crucial first make sure all the paths are proper and docker images and all the flow should be clear db is automatically crate all the data of images should maintain in the db of the docker image and it is very important that we have to mention the volumnes that are used in dags in folder that volumnes in docker file should be mention to import config all those things in the dags airflow should be very crucial on paths if we miss any thing it will break the pipeline and mention docker name before paths 

This is the flow of the web frame work
main.py  →  app.py  →  routes.py  →  services (like model_service.py, data_service.py)
