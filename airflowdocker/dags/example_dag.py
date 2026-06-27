from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="sales_order_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_spark = BashOperator(
        task_id="run_spark",
        bash_command="""
        spark-submit \
        --master spark://soumeshchnandradas-H310M-H:7077 \
        /opt/airflow/dags/test_pyspark.py
        """,
    )
