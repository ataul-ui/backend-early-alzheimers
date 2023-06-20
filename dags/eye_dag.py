from airflow import DAG
import json
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator

# Define database credentials
host = 'host.docker.internal'
port = '5432'
dbname = 'alzhimers'
user = 'airflow'
password = 'airflow'


def transcribe_file(**kwargs):
    context = kwargs
    context['ti'].xcom_push(key='mykey', value='ocular data has been received')
    return "ocular data has been received"


def score_data(**kwargs):
    ti = kwargs['ti']
    transcribed = ti.xcom_pull(key='mykey')
    print(transcribed)
    rest = ti.xcom_pull(task_ids=['load_file'])
    if not rest:
        raise Exception('No data.')
    else:
        return rest


def upload_to_postgre():
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "dags", "data", "example.json")
    
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO user_info (biomarker) VALUES (%s)", (json_data["biomarker"],))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return "will_upload"


with DAG("eye_pipeline", start_date=datetime(2021,1,1),
         schedule_interval='@daily', catchup=False) as dag:
    
    load_file = PythonOperator(
        task_id='load_file',
        python_callable=transcribe_file,
        do_xcom_push=True,
        provide_context=True
    )
    
    scored_result = PythonOperator(
        task_id='scored_result',
        python_callable=score_data,
        do_xcom_push=True,
        provide_context=True
    )
    
    database_upload = PythonOperator(
        task_id='database_upload',
        python_callable=upload_to_postgre
    )
    
    load_file >> scored_result >> database_upload
