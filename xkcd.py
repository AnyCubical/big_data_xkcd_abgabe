from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import asyncio
import requests
import json
import os
from pathlib import Path
from multiprocessing import Pool



args = {
    'owner': 'airflow'
}

def multi_downloader(i):
    if i != 404 and i != 1037 and i != 1331:
        jsonObj = requests.get(f'https://xkcd.com/{i}/info.0.json').json()

        if (os.path.exists(f'/home/airflow/xkcd/raw/{jsonObj["year"]}')):
            Path(f'/home/airflow/xkcd/raw/{jsonObj["year"]}/{jsonObj["num"]}.json').write_text(json.dumps(jsonObj))
        else:
            os.makedirs(f'/home/airflow/xkcd/raw/{jsonObj["year"]}')
            Path(f'/home/airflow/xkcd/raw/{jsonObj["year"]}/{jsonObj["num"]}.json').write_text(json.dumps(jsonObj))


def download_xkcd():
    lenReq = requests.get('https://xkcd.com/info.0.json')
    lenObj = lenReq.json()

    zahl = range(1, int(lenObj["num"])+1)
    pool = Pool()
    pool.map(multi_downloader, zahl)

dag = DAG('xkcd', default_args=args, description='xkcd comics',
          schedule_interval='56 18 * * *',
          start_date=datetime(2019, 10, 16), catchup=False, max_active_runs=1)

create_placeholder = BashOperator(
    task_id='create_placeholder_locally',
    bash_command='touch /home/airflow/xkcd/raw/placeholder',
    dag = dag
)

copy_hdfs_placeholder = BashOperator(
    task_id='copy_placeholder_to_hdfs',
    bash_command='/home/airflow/hadoop/bin/hadoop fs -put /home/airflow/xkcd/raw/placeholder /user/hadoop/xkcd/raw',
    dag = dag
)

clear_xkcddata = BashOperator(
    task_id='clear_xkcddata_locally',
    bash_command='rm -r /home/airflow/xkcd/raw/*',
    dag = dag
)

download_xkcd = PythonOperator(
    task_id='download_xkcd_locally',
    python_callable=download_xkcd,
    dag = dag
)

clear_xkcddata_hdfs = BashOperator(
    task_id='clear_xkcddata_in_hdfs',
    bash_command='/home/airflow/hadoop/bin/hadoop dfs -rm -r /user/hadoop/xkcd/raw',
    dag = dag
)

push_xkcddata_hdfs = BashOperator(
    task_id='push_xkcddata_to_hdfs',
    bash_command='/home/airflow/hadoop/bin/hadoop fs -put /home/airflow/xkcd /user/hadoop',
    dag = dag
)

pyspark_raw_to_final = SparkSubmitOperator(
    task_id='pyspark_raw_to_final',
    conn_id='spark',
    application='/home/airflow/airflow/python/finalizer.py',
    total_executor_cores='2',
    executor_cores='2',
    executor_memory='2g',
    num_executors='2',
    name='spark_raw_to_final',
    dag = dag
)

create_placeholder >> copy_hdfs_placeholder
copy_hdfs_placeholder >> clear_xkcddata_hdfs
copy_hdfs_placeholder >> clear_xkcddata >> download_xkcd
download_xkcd >> push_xkcddata_hdfs >> pyspark_raw_to_final
clear_xkcddata_hdfs >> push_xkcddata_hdfs
