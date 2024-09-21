import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from modules import create_table, insert_data, get_data, send_mail

load_dotenv()

default_args={
    'owner': 'MacarenaTaie',
    'retries':2,
    'retry_delay': timedelta(minutes=1),
    'email': [os.getenv("email")],
    'email_on_failure': True,
    'email_on_retry': True
}

with DAG(
    default_args=default_args,
    dag_id='ETL_Proyecto',
    description= 'DAG para proyecto final de Coderhouse',
    start_date=datetime(2024,9,19),
    schedule_interval='@daily',
    catchup=False
    ) as dag: 

    task1= PythonOperator(
        task_id='create_table',
        python_callable= create_table,
        dag=dag,
    )

    task2= PythonOperator(
        task_id='insert_data',
        python_callable= insert_data,
        dag=dag,
    )

    task3= PythonOperator(
        task_id='get_data',
        python_callable= get_data,
        dag=dag,
    )

    task4= PythonOperator(
        task_id='send_email',
        python_callable= send_mail,
        dag=dag,
    )

    task1 >> task2 >> task3 >> task4