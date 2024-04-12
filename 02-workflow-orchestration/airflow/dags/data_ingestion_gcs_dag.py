import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import requests
from google.cloud import storage

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'upload_and_load_yearly_bigquery_tables',
    default_args=default_args,
    description='Upload files to GCS and load into yearly BigQuery tables',
    schedule_interval='@daily',  # Adjust as necessary
)

def upload_files_to_gcs(**kwargs):
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now() - timedelta(days=1)  # Adjust as necessary
    client = storage.Client()
    bucket_name = 'network-performance-418402-bucket'  # Update this
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
                blob.upload_from_string(response.content, content_type='text/csv')
                print(f"Uploaded {gcs_path} to GCS bucket {bucket_name}")
            else:
                print(f"File not found at {file_url}")
        else:
            print(f"File {gcs_path} already exists in GCS bucket {bucket_name}")

        current_date += timedelta(days=1)

upload_files_task = PythonOperator(
    task_id='upload_files_to_gcs',
    python_callable=upload_files_to_gcs,
    dag=dag,
)

def load_year_to_bigquery(year, **kwargs):
    destination_table = f"network-performance-418402.network_performance.table_{year}"
    dataset_folder = f"gs://network-performance-418402-bucket/{year}/*/*.csv"  # Pattern to match all files for the year
    load_job = GCSToBigQueryOperator(
        task_id=f'load_{year}_to_bigquery',
        bucket='network-performance-418402-bucket',  # Update this
        source_objects=[f'{year}/*.csv'],  # Wildcard to select all months
        source_format='CSV',
        skip_leading_rows=1,  # Assuming the first row is header
        field_delimiter=',',
        destination_project_dataset_table=destination_table,
        write_disposition='WRITE_TRUNCATE',  # Overwrite the table if it exists
        create_disposition='CREATE_IF_NEEDED',
        dag=dag,
    )
    return load_job.execute(context=kwargs)

# Dynamically create tasks for loading data into yearly BigQuery tables
start_year = 2020
end_year = datetime.now().year  # Adjust as necessary to include 2024 if data is present
for year in range(start_year, end_year + 1):
    load_year_task = PythonOperator(
        task_id=f'load_{year}_to_bigquery_callable',
        python_callable=load_year_to_bigquery,
        op_kwargs={'year': year},
        provide_context=True,
        dag=dag,
    )
    upload_files_task >> load_year_task
