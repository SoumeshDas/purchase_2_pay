from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="spark_cluster_test",
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
) as dag:

    run_spark = BashOperator(
        task_id="run_spark",
        bash_command="""
                        /opt/spark/bin/spark-submit \
                        --master spark://spark-master:7077 \
                        /jobs/scripts/test_cluster.py
                    """
    )