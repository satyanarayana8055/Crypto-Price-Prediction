"""Airflow DAG for ETL pipeline"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml
from src.etl.extract import extract_coin_data
from src.etl.transform import transform_coin_data
from src.etl.load import load_to_db
from src.utils.logger import get_logger

logger = get_logger('etl_pipeline')

with open('/app/pipeline_config.yaml', 'r') as f: 
    config = yaml.safe_load(f)

default_args = {
    'owner': 'airflow',
    "retries": 3,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': lambda context: logger.error(f"Task failed: {context['task_instance'].task_id}")
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval=config['airflow']['etl_dag']['schedule'],
    catchup=False,
    description="ETL pipeline for cryptocurrency data"
)

def create_coin_tasks(coin: str):
    """Create ETL tasks for a coin"""
    start_date = ['airflow']['etl_dag']['start_date']
    end_date = ['airflow']['etl_dag']['end_date']
    extract_task = PythonOperator(
        task_id=f'extract_{coin}',
        python_callable=extract_coin_data,
        op_args=[coin, start_date, end_date],
        dag=dag,
        do_xcom_push=True
    )
    transform_task = PythonOperator(
        task_id=f'transform_{coin}',
        python_callable=transform_coin_data,
        op_args=["{{ ti.xcom_pull(task_ids='extract_"+coin+"') }}"],
        dag=dag
    )
    load_task = PythonOperator(
        task_id=f'load_{coin}',
        python_callable=load_to_db,
        op_args=["{{ ti.xcom_pull(task_ids='transform_"+coin+"') }}"],
        dag=dag
    )
    extract_task >> transform_task >> load_task
    return load_task

coin_tasks = [create_coin_tasks(coin) for coin in config['airflow']['etl_dag']['coins']]
logger.info("ETL pipeline DAG initialized")