# NBA_pipeline01

![nba_project_pic](https://user-images.githubusercontent.com/105791967/219845142-339ded9c-fd49-4cfe-a0e9-7247c0d00499.jpg)

This project scraped data from https://www.basketball-reference.com stored in database and ELT to do transformation in Databricks save it as a delta table to make some prediction.

I already test this project and it can do ETL to S3 bucket without problem

## Step to run this project
If you want to test this yourself. You must have AWS account and create S3 bucket then edit some credential in dags.py and you have to craete .env file for others credential to run this project.
1. run 	`docker-compose -f db.yml` to first build Postgres database with web-scrapped data
2. iIn another terminal run 	`docker-compose up -d` to run Airflow. Go to localhost:8080 and feel free to Trigger DAGS
