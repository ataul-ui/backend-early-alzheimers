from datetime import datetime, timedelta
import psycopg2
import os
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# define database credentials
host = 'host.docker.internal'
port = '5432'
dbname = 'alzhimers'
user = 'airflow'
password = 'airflow'

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
    
    # Get contents of json file
    file_path = os.path.join(os.getcwd(), "dags", "data", "create_database.json")
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
    # create a cursor object to interact with the database
    cur = conn.cursor()
    # Create the fact table
    cur.execute("""
        DROP TABLE IF EXISTS user_info;
                
        CREATE TABLE user_info (
            username VARCHAR(10),
            password VARCHAR(10),
            age INT,
            sex VARCHAR(10),
            biomarker INT,
            score INT,
            hrv INT,
            country VARCHAR(50)
        );
    """)
    
    # Add the json data to the fact table
    cur.execute(
        "INSERT INTO user_info (username, password, age, sex, country) VALUES (%s, %s, %s, %s, %s)",
        (json_data["username"], json_data["password"], json_data["age"], json_data["sex"], json_data["country"])
    )
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
create_regular_schema_task = PythonOperator(
    task_id='create_star_schema',
    python_callable=create_star_schema,
    dag=dag
)

# set the order of the tasks in the DAG
create_regular_schema_task


