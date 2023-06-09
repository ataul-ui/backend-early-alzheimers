from airflow import DAG
from datetime import datetime, timedelta 
from airflow.operators.python_operator import PythonOperator
import openai


def transcribe_file(**kwargs):
    context = kwargs
    context['ti'].xcom_push(key='mykey', value='I like like like to eat not eat ice cream and fly to brazil')
    return "Text data has been transcribed"

def score_data(**kwargs):
    ti = kwargs['ti']
    transcribed = ti.xcom_pull(key='mykey')
    
    openai.api_key = "my quota has ended, use your own key through environment variable"
    
    response = openai.Completion.create(
        model="text-curie-001",
        prompt="Please rate the natural language quality of the following text on a scale of 1 to 10, with 1 being very bad and 10 being very good: " + transcribed,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    irregularities = response.choices[0]
    
    context = kwargs
    context['ti'].xcom_push(key='data_key', value=irregularities)

def upload_to_postgre(**kwargs):
    ji = kwargs['ti']
    uploaded = ji.xcom_pull(key='data_key')
    print(uploaded)
    # Will upload to the database using SQL code
    
    return uploaded


with DAG("speech_pipeline", start_date=datetime(2021, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    
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
        python_callable=upload_to_postgre,
        provide_context=True
    )

load_file >> scored_result >> database_upload

