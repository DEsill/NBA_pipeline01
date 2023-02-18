from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago
import psycopg2
import boto3
import os
import csv
from dotenv import load_dotenv

load_dotenv()

class Config:
    POSTGRES_USER_S = os.getenv("POSTGRES_USER_S")
    POSTGRES_PASSWORD_S = os.getenv("POSTGRES_PASSWORD_S")
    POSTGRES_DB_S = os.getenv("POSTGRES_DB_S")
    POSTGRES_HOST_S = os.getenv("POSTGRES_HOST_S")
    POSTGRES_PORT_S = os.getenv("POSTGRES_PORT_S")

def load_data_to_s3():
    # Connect to the database
    conn = psycopg2.connect(database = Config.POSTGRES_DB_S, 
                            user = Config.POSTGRES_USER_S, 
                            password = Config.POSTGRES_PASSWORD_S, 
                            host = Config.POSTGRES_HOST_S, 
                            port = Config.POSTGRES_PORT_S
                            )

    # Set the name of the S3 bucket and the path where you want to mount it
    bucket_name = "sill-databricks-projects"
    #mount_point = '/mnt/sill-databricks-projects'
    REGION = "ap-southeast-1"

    # Set the AWS access key ID and secret access key
    ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")

    file_name = ["mvps_hot", "players_cold", "teams_cold"]
    table_name = ["mvps", "players", "teams"]

    for file, table in zip(file_name, table_name):
        # Open a cursor to perform database operations
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {table};")
        column_names = [desc[0] for desc in cur.description]

        # Fetch the results of the query
        results = cur.fetchall()

        with open(f"/home/airflow/data/{file}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(results)

    cur.close()
    conn.close()

    # Upload the CSV file to Amazon S3
    s3 = boto3.client(
        "s3",
        region_name=REGION,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
    )
    s3.upload_file("/home/airflow/data/mvps_hot.csv", "sill-databricks-projects", "mvps_hot.csv")
    s3.upload_file("/home/airflow/data/players_cold.csv", "sill-databricks-projects", "players_cold.csv")
    s3.upload_file("/home/airflow/data/teams_cold.csv", "sill-databricks-projects", "teams_cold.csv")

with DAG(
    dag_id = 'nba_stats_pipline',
    start_date = days_ago(1),
    schedule_interval = '@once'
) as dag:

    load_data_to_s3_task = PythonOperator(
        task_id = 'load_data_to_s3',
        python_callable = load_data_to_s3
    )

load_data_to_s3_task