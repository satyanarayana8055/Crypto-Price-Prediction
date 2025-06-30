from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml
from monitoring.drift_analysis import analyze_drift
from monitoring.performance_metrics import monitor_metrics
from utils.logger import get_logger 

logger = get_logger('monitor_pipeline')

with open('/app/dags/dag_config.yml', 'r') as f: 
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
    metrics_task = PythonOperator(
        task_id=f'log_metrics_{coin}',
        python_callable=monitor_metrics,
        op_args=[coin],
        dag=dag
    )
    drift_task = PythonOperator(
        task_id = f'drift_{coin}',
        python_callable=analyze_drift,
        op_args=[coin ],
        dag=dag
    )
    metrics_task >> drift_task
    return  drift_task

coin_tasks = [create_coin_tasks(coin) for coin in config['airflow']['monitor_dag']['coins']]
logger.info("Monitor pipeline DAG initialized")