# backend-early-alzheimers

testing something again
blah baassl
uhh what?
THIS IS A DATAOPS PROJECT, I WILL EXPLAIN MORE IN THE MEDIUM ARTICLE

Y'know I think I'd rather use google drive, 
so I can follow that tutorial directly

^^^ use dvc directly on dockerfile
and airflow task, follow this link for help: https://medium.com/analytics-vidhya/docker-volumes-with-dvc-for-versioning-data-and-models-for-ml-projects-4885935db3ec 

make sure you have docker installed

First clone this repository
make a copy of .env.example file and name it .env
then add in your credentials

run docker compose up and you should be good
airflow trigger github actions in order to upload to azure
using shell commands



I think I can use github actions to upload the data to azure, use dvc for it maybe
Right, I think github actions can be used to do dvc which then uploads data to azure blob storage, that actually sounds pretty good

Airflow will run when triggered, dvc will run once a week

Tests will depend on country and culture, to see tests that my group did for US patients follow this link: https://github.com/ataul-ui/novo-early-alzhimers 

This repository contains the backend code for an early Alzheimer's detection system. The system is designed to analyze various data sources, such as ocular data, speech data, and stress data, to detect early signs of Alzheimer's disease in individuals.

Features
Ocular Data Analysis: The system processes ocular data to identify potential biomarkers associated with Alzheimer's disease. It transcribes the received data and performs analysis to extract relevant information.

Speech Data Analysis: Speech data is analyzed to detect speech patterns and anomalies that may indicate early signs of Alzheimer's disease. The system evaluates picture accuracy, verbal fluency, verbal richness, stutters/fillers, and speech errors.

Stress Data Analysis: The system assesses stress levels based on collected data. It calculates average heart rate, heart rate variability, and galvanic skin response to identify patterns related to Alzheimer's disease.

Star Schema Database: The backend creates a star schema in a PostgreSQL database to store the processed data. The schema includes tables for ocular data, speech data, stress data, and user information. Foreign key constraints are defined to ensure data integrity.

Installation
Clone the repository: git clone https://github.com/ataul-ui/backend-early-alzheimers.git
Install the required dependencies: pip install -r requirements.txt
Set up the PostgreSQL database with the provided credentials (host, port, dbname, user, password).
Configure the system parameters and database credentials in the code files.
Run the backend system: docker-compose up --build
Usage
Ensure that the data sources (ocular data, speech data, stress data) are properly configured and accessible.
Start the backend system, which will process the data and store the results in the PostgreSQL database.
Use the created star schema database to perform data analysis, generate insights, and detect early signs of Alzheimer's disease.
Contributing
Contributions to this project are welcome. If you have suggestions for new features, bug fixes, or improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code for your own purposes.

sdds