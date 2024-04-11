import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
from google.cloud import storage

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def upload_files_to_gcs():
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now() - timedelta(days=1)  # Yesterday
    
    # Initialize the GCS client
    client = storage.Client()
    bucket_name = 'network-performance-418402-bucket'
    bucket = client.bucket(bucket_name)

    current_date = start_date
    while current_date <= end_date:
        year, month, day = current_date.strftime("%Y"), current_date.strftime("%m"), current_date.strftime("%d")
        file_url = f"https://github.com/kahramanmurat/network-performance-data/raw/main/{year}/{month}/performance_data_{year}-{month}-{day}.csv"
        gcs_path = f"{year}/{month}/performance_data_{year}-{month}-{day}.csv"

        blob = bucket.blob(gcs_path)
        if not blob.exists():
            response = requests.get(file_url)
            if response.status_code == 200:
                blob.upload_from_string(response.content)
                print(f"Uploaded {gcs_path} to GCS bucket {bucket_name}")
            else:
                print(f"File not found at {file_url}")
        else:
            print(f"File {gcs_path} already exists in GCS bucket {bucket_name}")

        current_date += timedelta(days=1)

dag = DAG(
    'upload_to_gcs_if_not_exists',
    default_args=default_args,
    description='Upload files to GCS if they do not exist',
    schedule_interval='0 9 * * *',  # Set to run daily at 9 AM
)

task = PythonOperator(
    task_id='upload_files_to_gcs',
    python_callable=upload_files_to_gcs,
    dag=dag,
)
