from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from etl import create_table, insert_data


default_args={
    'owner': 'MacarenaTaie',
    'retries':5,
    'retry_delay': timedelta(minutes=3)
}

dag_coder = DAG(
    default_args=default_args,
    dag_id='ETL_Proyecto',
    description= 'DAG para proyecto final de Coderhouse',
    start_date=datetime(2024,9,4),
    schedule_interval='@daily'
    )
    
task1= PythonOperator(
    task_id='create_table',
    python_callable= create_table,
    dag=dag_coder,
)

task2= PythonOperator(
    task_id='insert_data',
    python_callable= insert_data,
    dag=dag_coder,
)

task1 >> task2