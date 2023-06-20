from datetime import datetime, timedelta
import os
import json
import psycopg2
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define database credentials
host = 'host.docker.internal'
port = '5432'
dbname = 'alzhimers'
user = 'airflow'
password = 'airflow'


def create_star_schema():
    # Create a connection to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    # Define the queries for creating tables
    table_queries = [
        """
        DROP TABLE IF EXISTS stress;
        CREATE TABLE stress (
            username VARCHAR(50),
            test_date TIMESTAMP,
            average_bpm DECIMAL,
            average_hrv DECIMAL,
            average_gsr DECIMAL
        )
        """,
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            username VARCHAR PRIMARY KEY,
            password VARCHAR,
            age INTEGER,
            gender VARCHAR,
            education_level VARCHAR
        )
        """,
        """
        DROP TABLE IF EXISTS tests;
        CREATE TABLE tests (
            username VARCHAR(50),
            test_date TIMESTAMP,
            gaze_successful_tracks INTEGER,
            gaze_unsuccessful_tracks INTEGER,
            gaze_variance DECIMAL,
            vstm_total_correct SMALLINT,
            vstm_total_correct_simple_correct SMALLINT,
            vstm_total_correct_complex_correct SMALLINT,
            vstm_total_correct_average_delay DECIMAL
        )
        """,
        """
        DROP TABLE IF EXISTS speech;
        CREATE TABLE speech (
            username VARCHAR(50),
            test_date TIMESTAMP,
            picture_accuracy INTEGER,
            picture_verbal_fluency INTEGER,
            picture_verbal_richness INTEGER,
            picture_stutters_fillers INTEGER,
            picture_speech_errors INTEGER
        )
        """
    ]
    
    # Create a cursor object to interact with the database
    cur = conn.cursor()
    
    # Execute the table creation queries
    for query in table_queries:
        cur.execute(query)
    
    # Create the foreign key constraints
    cur.execute("""
        ALTER TABLE tests
        ADD CONSTRAINT tests_username_fkey
        FOREIGN KEY (username)
        REFERENCES users(username)
    """)
    
    cur.execute("""
        ALTER TABLE speech
        ADD CONSTRAINT speech_username_fkey
        FOREIGN KEY (username)
        REFERENCES users(username)
    """)
    
    cur.execute("""
        ALTER TABLE stress
        ADD CONSTRAINT stress_username_fkey
        FOREIGN KEY (username)
        REFERENCES users(username)
    """)
    
    # Commit the changes to the database and close the connection
    conn.commit()
    cur.close()
    conn.close()


# Define the DAG
default_args = {
    'owner': 'ataul',
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


# Define the operator that will run the task
create_star_schema_task = PythonOperator(
    task_id='create_star_schema',
    python_callable=create_star_schema,
    dag=dag
)

# Set the order of the tasks in the DAG
create_star_schema_task
