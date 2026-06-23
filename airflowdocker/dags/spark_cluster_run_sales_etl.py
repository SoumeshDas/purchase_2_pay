from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="spark_cluster_run_sales_etl",
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
) as dag:

    run_spark = BashOperator(
        task_id="run_spark",
        bash_command="""
                        docker exec -i spark-master \
                        /opt/spark/bin/spark-submit \
                        --master spark://spark-master:7077 \
                        --total-executor-cores 1 \
                        --executor-memory 512m \
                        /jobs/scripts/sales_etl.py
                    """
    )