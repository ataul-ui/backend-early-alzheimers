




#FROM puckel/docker-airflow:1.10.9
#RUN pip install psycopg2-binary

FROM puckel/docker-airflow:1.10.9

RUN pip install psycopg2-binary==2.8.6 --no-cache-dir



RUN pip install requests
RUN pip install python-dotenv
RUN pip install dvc[all]
RUN pip install dvc[azure]
ENV PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin/dvc:${PATH}"

#RUN dvc --version


# dvc location: /Library/Frameworks/Python.framework/Versions/3.10/bin/dvc
#RUN which dvc
#RUN dvc --version
#RUN pip install --upgrade pip
#RUN pip install psql[all]
