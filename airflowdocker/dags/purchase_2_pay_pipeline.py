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
    tags=["kafka", "spark", "streaming"],
) as dag:

    produce_sales = BashOperator(
        task_id="produce_sales",
        bash_command="""
        docker run --rm \
        --network kafka-docker_default \
        -e KAFKA_SERVER=kafka:9092 \
        -v /home/soumeshchnandradas/source_code/purchase_2_pay_solution:/jobs \
        kafka-python-docker:1.0 \
        python /jobs/scripts/produce_sales.py
        """
    )

    wait_for_stream = BashOperator(
        task_id="wait_for_stream",
        bash_command="""
        sleep 15
        """
    )

    soda_scan = BashOperator(
        task_id="soda_scan",
        bash_command="""
        echo "Run Soda Scan here"
        """
    )

    notify = BashOperator(
        task_id="notify",
        bash_command="""
        echo "Pipeline Completed Successfully"
        """
    )

    produce_sales >> wait_for_stream >> soda_scan >> notify