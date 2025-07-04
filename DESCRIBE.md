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
│   ├── api/                         # Web API (Flask app)
│   │   ├── __init__.py              # Initializes Flask API package
│   │   ├── app.py                   # Flask app factory (creates app instance)
│   │   ├── routes.py                # Defines web routes/endpoints (e.g., /predict)
│   │   ├── static/                  # Static files (CSS, JS)
│   │   │   ├── css/
│   │   │   └── js/
│   │   ├── templates/               # HTML templates for Flask (e.g., index.html)
│   ├── services/                    # Business logic services
│   │   ├── __init__.py
│   │   ├── model_service.py         # Loads model and makes predictions
│   │   ├── notify_service.py        # Sends alerts/notifications
│   │   ├── data_service.py          # Fetches latest crypto data
│   │   └── data_drift.py            # Custom error handling
│   └── main.py                      # Entrypoint for web app

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
├── README.md                        # Project overview/documentation
├── requirements.txt                 # Python dependencies
├── setup.py                         # Project metadata/setup (if using build system)

# setup instructions
1. Clone the Repository
git clone repo link
cd to repo name

2. Create conda envnirnment 
conda create -n crypto python=3.10

3. Create requirements.txt

Next, create a setup.py file to treat every script as a package — useful for cleaner imports and Docker compatibility.
The setup.py file allows you to import any required file as a module. This means you no longer need to write the full import path.
from src.scripts.data_ingestion import load_data
from data_ingestion import load_data
pip install -e .

4. Set Up config.py and pipeline_config.yaml

Create a config.py file to support modular coding and avoid hardcoding values across the project.
This acts as a central controller, where all key parameters (like database credentials, file paths, API keys, etc.) can be managed and modified easily.
Also, use pipeline_config.yaml to configure pipeline-related settings.
This YAML file is human-readable, and it's especially useful for tools like Airflow and Docker, making your project environment-agnostic and easy to adapt for local or cloud deployment.

5. Set up logger file it is very import to mention loggers in every peice of because it is import to track the flow and where we get the error because of logs we can do the debuging easily

6. Create .env file for secure the Keys and Passwords

7. Set up gitigone file to ignore tracking of not need files and folders

8. Set Up PostgreSQL (Optional for Local Testing Only)

If you are testing your project locally without Docker, you can manually set up PostgreSQL on your system:
🛠️ PostgreSQL Manual Setup Steps
Switch to the Postgres user:
sudo -i -u postgres
Access the PostgreSQL shell:
psql
Create a new user and database:
sql

-- Create a user with a password
CREATE USER api_user WITH PASSWORD '1234';

-- Create a new database and assign ownership to the user
CREATE DATABASE api_db OWNER api_user;

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON DATABASE api_db TO api_user;

9. Database Setup in Real-World Projects (Using Docker)
In real-world production environments, you should not create the database locally on your host machine. Instead, you should use Docker containers to run and manage all database services (e.g., PostgreSQL).
🔍 Accessing and Exporting Data from Docker PostgreSQL
To access your database and export data from within a container:
Open a shell into the PostgreSQL container:
docker exec -it <container_id_or_name> bash
Log in to PostgreSQL using credentials:
psql -U crypto_user -d crypto_db

Export data from any table (replace your_table_name.csv accordingly)
COPY your_table_name TO '/tmp/your_table_name.csv' WITH CSV HEADER;

Copy the CSV file from the container to your local system:
docker cp pg_container:/tmp/your_table_name.csv ./your_table_name.csv


10. Airflow Integration and Best Practices
Airflow plays a critical role in automating ETL, model training, and monitoring tasks. However, to ensure smooth execution, it's important to follow these best practices:

✅ Correct Path Management: All paths referenced in Airflow DAGs (like for data, configs, or logs) must be correct and accessible within the Docker container. Inconsistent or incorrect paths will cause the pipeline to fail.
✅ Docker Volumes: Make sure to mount volumes properly in docker-compose.yml so that the Airflow containers can access your DAGs, configuration files, and output directories.
✅ Database Setup: Airflow creates and uses its metadata database automatically. If you want to store pipeline-related data (e.g., from ETL), make sure to:

Use the PostgresHook in your Airflow tasks.
Provide valid PostgreSQL database credentials in Airflow's webserver environment (via .env or airflow.cfg).
Mount and connect to the PostgreSQL container running in Docker.
🧠 If any path or volume is missed or incorrectly set, the DAGs will fail during execution. Always prefix container-level paths with the correct Docker volume name or Docker service path to avoid issues.


11. Model Pipeline and MLflow Integration
After automating the ETL and preprocessing tasks, the next step is to build the model pipeline. Although the structure and flow of tasks remain similar to previous steps, this stage focuses on training and evaluating machine learning models.

To enhance this process, MLflow is integrated to:
Track different experiments
Compare models trained with various hyperparameters
Log performance metrics and artifacts (like models, plots)
Choose the best-performing model based on evaluation results

✅ MLflow is extremely useful in experiment tracking and helps in selecting the best model for deployment with transparency and reproducibility.
12. Flask Framework
Flask is used in this project to expose all your data workflows, model predictions, and monitoring results through a simple web interface. It acts as the frontend for all your backend logic and machine learning pipelines.

🔍 Note: Flask in this project primarily supports read operations — meaning it reads data from the database or files and displays it on the web. It doesn't perform heavy data loading or training directly.

The routes (defined in routes.py) act as API endpoints. These routes retrieve data from the database or services and serve it to the web UI for display.

🔁 Flask Workflow
main.py  →  app.py  →  routes.py  →  services/
                               ├── model_service.py
                               ├── data_service.py
                               └── notify_service.py

main.py: Entry point for the Flask application
app.py: Initializes the app and config
routes.py: Defines API endpoints

services/: Contains the business logic for fetching predictions, data, and notifications
13. Docker is used in this project to orchestrate multiple services such as Airflow, MLflow, PostgreSQL, and the Flask web application.

⚠️ Important Considerations:

If you store your data inside the PostgreSQL Docker container, that container must remain running continuously — you cannot access or test data through the terminal after the container stops. This is a common issue when using containers for data persistence.

If you plan to use multiple services (like Airflow, MLflow, and Flask), it's best to create separate Dockerfiles or services for each in your docker-compose.yml. Trying to run everything from a single Dockerfile can lead to compatibility and networking issues.

To handle all services together, use a central bash script as the entry point. This script should orchestrate the startup of all services in the correct order.

Finally, when using Docker, mount volumes properly. If volumes are not correctly mapped, the Docker containers will not have access to your project's data, configurations, or logs — leading to runtime errors or missing outputs.


14. GitHub Actions CI/CD is a critical part of the project. It automates two main stages: testing and deployment.

During testing, GitHub Actions ensures that the flow of data, model training, and web application behavior remains consistent with previous versions — this is crucial for maintaining reproducibility and stability.

Deployment creates a full Docker image of the project, which is then pushed to Docker Hub for continuous delivery.

⚠️ Note: GitHub Actions does not store data — it only works with what’s available in the local environment (VS Code) or on cloud storage/services. So, storing data in local databases or Docker container volumes can lead to issues if not handled properly. Ensure that critical data is persisted and available during workflow runs.

The final image is a Flask-based Docker image that runs the entire project via a web UI and is kept up-to-date through automated CI/CD pipelines.

15. The monitoring component of the project is implemented using Evidently. It generates an HTML report that displays feature distributions, data drift, and performance monitoring. When this HTML is rendered via a route in the web app, it visualizes these insights interactively. Additionally, if the model's performance metrics drop significantly, the web service sends an email notification alerting the user.


