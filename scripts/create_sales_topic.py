from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
"owner": "soumesh",
}

with DAG(
dag_id="purchase_2_pay_pipeline",
start_date=datetime(2026, 1, 1),
schedule=None,
catchup=False,
default_args=default_args,
tags=["kafka", "spark", "airflow"],
) as dag:


    create_sales_topic = BashOperator(
        task_id="create_sales_topic",
        bash_command="""
        python /jobs/scripts/create_sales_topic.py
        """
    )
