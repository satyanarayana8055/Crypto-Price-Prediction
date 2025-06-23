"""Airflow DAG for model training"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml
from pipeline.preprocessing import preprocess_data
from pipeline.feature_extraction import extract_features
from pipeline.model import train_model
from pipeline.evaluate import evaluate_model
from utils.logger import get_logger

logger = get_logger('dags')

with open('/app/dags/dag_config.yaml', 'r') as f:  # Use absolute path
    config = yaml.safe_load(f)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'model_pipeline',
    default_args=default_args,
    schedule_interval=config['airflow']['model_dag']['schedule'],
    catchup=False, # while runing airflow we missing some data if it is false leave that missed data and continue or if it is ture then it has to get all the data without missing
    description="Model training pipeline for cryptocurrency data"
)

def create_coin_tasks(coin: str):
    """Create model trianing tasks for a coin"""

    preprocess_task = PythonOperator(
        task_id=f'preprocess_{coin}',
        python_callable=preprocess_data,
        op_args=[coin],
        dag = dag,
    )
    feature_task = PythonOperator(
        task_id=f'feature_extraction_{coin}',
        python_callable=extract_features,
        op_args=[coin],
        dag=dag,
    )
    train_task = PythonOperator(
        task_id = f'train_{coin}',
        python_callable=train_model,
        op_kwargs={'coin': coin, 'hyperparams': config['airflow']['model_dag']['hyperparams']},
        dag=dag,
    )
    evaluate_task = PythonOperator(
        task_id=f'evaluate_{coin}',
        python_callable=evaluate_model,
        op_args=[coin],
        dag=dag
    )
    preprocess_task  >> feature_task  >> train_task >> evaluate_task
    return evaluate_task
coin_tasks = [create_coin_tasks(coin) for coin in config['airflow']['model_dag']['coins']]
logger.info("Model pipeline DAG initialized")
