from datetime import datetime, timedelta
import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# define database credentials
host = 'your_db_host'
port = 'your_db_port'
dbname = 'your_db_name'
user = 'your_db_username'
password = 'your_db_password'

# define the tasks for creating the star schema
def create_star_schema():
    # create a connection to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    # create a cursor object to interact with the database
    cur = conn.cursor()
    # create the dimension tables
    cur.execute("""
        CREATE TABLE eye_data (
            reference_eye SERIAL PRIMARY KEY,
            date DATE,
            biomarker INT
        );
        CREATE TABLE speech_data (
            reference_speech SERIAL PRIMARY KEY,
            date DATE,
            score INT
        );
        
        CREATE TABLE heart_data (
            reference_heart SERIAL PRIMARY KEY,
            date DATE,
            hrv INT
        );
    """)
    # create the fact table
    cur.execute("""
        CREATE TABLE user_info (
            username SERIAL PRIMARY KEY,
            password VARCHAR(10),
            age INT,
            sex VARCHAR(10),
            country VARCHAR(50)
        );
    """)
    # commit the changes to the database and close the connection
    conn.commit()
    cur.close()
    conn.close()

# define the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'create_star_schema',
    default_args=default_args,
    description='Create a star schema in PostgreSQL',
    schedule_interval=None
)

# define the operator that will run the task
create_star_schema_task = PythonOperator(
    task_id='create_star_schema',
    python_callable=create_star_schema,
    dag=dag
)

# set the order of the tasks in the DAG
create_star_schema_task


