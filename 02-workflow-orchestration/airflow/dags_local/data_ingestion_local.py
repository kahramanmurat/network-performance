import os

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script import ingest_callable


# Get PostgreSQL port from environment variables with default value

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT =  os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')



local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval=None,
    start_date=datetime(2021, 4, 28),
    catchup=False
)


URL_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow' 
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_2019-01.csv.gz'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_2019-01.csv.gz'
TABLE_NAME_TEMPLATE = 'yellow_taxi_2019-01'

with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
    )

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            csv_file=OUTPUT_FILE_TEMPLATE
        ),
    )

    wget_task >> ingest_task