from airflow import DAG
import json
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator

#LET THERE ONLY BE ONE DAG FI.E, AND IT SHOULD BE THIS ONE
#COMBINE IT WITH SPEECH_DAY.py
load_dotenv()
DB = os.getenv("dbname")

# Define database credentials
host = 'host.docker.internal'
port = '5432'
dbname = DB
user = 'airflow'
password = 'airflow'
    
def upload_to_postgre_speech_data(**kwargs):
    cwd = os.getcwd()
    file_path_speech = os.path.join(cwd, "dags", "data", "speech_data.json")
    
    with open(file_path_speech, "r") as json_file_speech:
        json_data_speech = json.load(json_file_speech)
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO user_info (score) VALUES (%s)", (json_data_speech["score"],))
    
    conn.commit()
    cur.close()
    conn.close()
    
    context = kwargs
    context['ti'].xcom_push(key='speechData', value='speech data has been received')
    
    return "uploaded speech data"


def upload_to_postgre_eye_data(**kwargs):
    cwd = os.getcwd()
    file_path_eye = os.path.join(cwd, "dags", "data", "ocular.json")
    
    with open(file_path_eye, "r") as json_file_eye:
        json_data_eye = json.load(json_file_eye)
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO user_info (biomarker) VALUES (%s)", (json_data_eye["biomarker"],))
    
    conn.commit()
    cur.close()
    conn.close()
    
    context = kwargs
    context['ti'].xcom_push(key='eyeData', value='ocular data has been received')
    
    return "will_upload"

def confirm_data_upload(**kwargs):
    ti = kwargs['ti']
    recieved_speech = ti.xcom_pull(key='speechData')
    recieved_eye = ti.xcom_pull(key='eyeData')
    
    
    print(recieved_speech)
    print(recieved_eye)
    
def dvc_github_actions_execute():
    return "something"


with DAG("eye_pipeline", start_date=datetime(2021,1,1),
         schedule_interval='@daily', catchup=False) as dag:
    
    database_upload_eye = PythonOperator(
        task_id='database_upload_eye',
        python_callable=upload_to_postgre_eye_data,
        do_xcom_push=True,
        provide_context=True
    )
    
    database_upload_speech = PythonOperator(
        task_id='database_upload_speech',
        python_callable=upload_to_postgre_speech_data,
        do_xcom_push=True,
        provide_context=True
    )
    
    confirmation_task = PythonOperator(
        task_id='confirmation_task',
        python_callable=confirm_data_upload,
        do_xcom_push=True,
        provide_context=True
    )
    
    dvc_github_actions = PythonOperator(
        task_id='dvc_github_actions',
        python_callable=confirm_data_upload
    )
    
    [database_upload_eye, database_upload_speech] >> confirmation_task >> dvc_github_actions
