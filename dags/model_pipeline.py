"""Airflow DAG for model training"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml
from src.scripts.ingestion import ingest_data
from src.scripts.preprocessing import preprocess_data
from src.scripts.feature_extraction import extract_features
from src.scripts.model import train_model
from src.utils.logger import get_logger

logger = get_logger('model_pipeline')
with open('/pipeline_config/pipeline_config.yaml', 'r') as f:  # Use absolute path
    config = yaml.safe_load(f)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'model_pipeline',
    default_args=default_args,
    schedule_interval=config['airflow']['model_dag']['schedule'],
    catchup=False # while runing airflow we missing some data if it is false leave that missed data and continue or if it is ture then it has to get all the data without missing
)

def create_coin_tasks(coin: str):
    """Create model trianing tasks for a coin"""
    ingest_task = PythonOperator(
        task_id = f'ingest_{coin}',
        python_callable=ingest_data,
        op_args=[coin],
        dag=dag
    )
    preprocess_task = PythonOperator(
        task_id=f'preprocess_{coin}',
        python_callable=preprocess_data,
        op_args=[ingest_task.output],
        dag = dag
    )
    feature_task = PythonOperator(
        task_id=f'feature_extraction_{coin}',
        python_callable=extract_features,
        op_args=[preprocess_task.output[0]],
        dag=dag
    )
    train_task = PythonOperator(
        task_id = f'train_{coin}',
        python_callable=train_model,
        op_args=[feature_task.output, coin, config['airflow']['model_dag']['hyperparams']],
        dag=dag
    )
    ingest_task >> preprocess_task >> feature_task >> train_task 
    return train_task
coin_tasks = [create_coin_tasks(coin) for coin in config['airflow']['model_dag']['coins']]
logger.info("Model pipeline DAG initialized")
