from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import timedelta

default_args = {
    "owner": "soumesh",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

PROJECT_ROOT = "/home/soumeshchnandradas/source_code/purchase_2_pay_solution"

with DAG(
    dag_id="purchase_2_pay_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["kafka", "spark", "streaming"],
) as dag:
    
    create_topic = BashOperator(
        task_id = "create_topic",
        bash_command = f"""docker run --rm \
        --network kafka-docker_default \
        -e KAFKA_SERVER=kafka:9092 \
        -v {PROJECT_ROOT}:/jobs \
        kafka-python-docker:1.0 \
        python /jobs/scripts/utilities/create_sales_topic.py"""
    )

    produce_sales = BashOperator(
        task_id="produce_sales",
        bash_command=f"""
        docker run --rm \
        --network kafka-docker_default \
        -e KAFKA_SERVER=kafka:9092 \
        -v {PROJECT_ROOT}:/jobs \
        kafka-python-docker:1.0 \
        # python /jobs/scripts/producer/produce_sales.py
        """,
        execution_timeout=timedelta(minutes=5)

    )

    wait_for_stream = BashOperator(
        task_id="wait_for_stream",
        bash_command=f"""
        docker run --rm \
        --network kafka-docker_default \
        -v {PROJECT_ROOT}:/jobs \
        kafka-python-docker:1.0 \
        python /jobs/scripts/utilities/wait_for_stream.py
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

    create_topic >> produce_sales >> wait_for_stream >> soda_scan >> notify