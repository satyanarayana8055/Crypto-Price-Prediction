from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml
import os
import joblib
from src.scripts.ingestion import ingest_data
from src.monitoring.drift_analysis import analyze_drift
from src.monitoring.performance_metrics import log_performance
from src.scripts.evaluate import evaluate_model
from src.utils.logger import get_logger 

logger = get_logger('monitor_pipeline')

with open('/app/pipeline_config.yaml', 'r') as f: 
    config = yaml.safe_load(f)
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(
    'monitor_pipeline',
    default_args=default_args,
    schedule_interval=config['airflow']['monitor_dag']['schedule'],
    catchup=False
)

def create_coin_tasks(coin: str):
    """Create monitoring tasks for a coin"""
    ingest_task = PythonOperator(
        task_id = f'ingest_{coin}',
        python_callable=ingest_data,
        op_args=[coin],
        dag=dag
    )
    drift_task = PythonOperator(
        task_id = f'drift_{coin}',
        python_callable=analyze_drift,
        op_args=[ingest_task.output, ingest_task.output, coin ],
        dag=dag
    )
    evaluate_task = PythonOperator(
        task_id = f'evaluate_{coin}',
        python_callable=evaluate_model,
        op_args=[coin, ingest_task.output],
        dag=dag
    )
    log_task = PythonOperator(
        task_id=f'log_metrics_{coin}',
        python_callable=log_performance,
        op_args=[evaluate_task.output, coin],
        dag=dag
    )
    ingest_task >> [drift_task, evaluate_task] >> log_task
    return log_task , drift_task
coin_tasks = [create_coin_tasks(coin) for coin in config['airflow']['monitor_dag']['coins']]
logger.info("Monitor pipeline DAG initialized")