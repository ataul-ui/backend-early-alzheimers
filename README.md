# backend-early-alzheimers

This repository contains the backend code for an early Alzheimer's detection system utilizing the DataOps approach. A detailed blog of this project is available [here](https://medium.com/@ataul.akbar/cost-effective-data-collection-for-alzheimers-disease-prevention-dataops-approach-7f9384f85d5).

### Requirements
Make sure you have docker installed. Follow this link to download it if you don't have it installed: https://www.docker.com/products/docker-desktop/



## Credentials
make a copy of .env.example file and name it .env
then add in your credentials


## Docker instructions
- To build and start the container

``` bash
docker-compose up --build 
```

- To stop container

``` bash
docker-compose down 
```

## Airflow UI access
Type ``` localhost:8080 ``` on any browser to access the airflow webserver UI



