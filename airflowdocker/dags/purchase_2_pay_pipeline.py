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

    load_to_duckdb = BashOperator(
        task_id="load_to_duckdb",

        bash_command=f"""
        docker run --rm \
        -v {PROJECT_ROOT}:/jobs \
        soda-custom:latest \
        python /jobs/scripts/utilities/load_bronze_to_duckdb.py
        """
    )

    soda_scan = BashOperator(
        task_id="run_soda",
        bash_command=f"""
        docker run --rm \
        -v {PROJECT_ROOT}:/jobs \
        soda-custom:latest \
        python /jobs/scripts/quality/run_soda.py
        """
    )

    notify = BashOperator(
        task_id="notify",
        trigger_rule="all_done",
        bash_command=f"""
        docker run --rm \
        -v {PROJECT_ROOT}:/jobs \
        -e GMAIL_USER=$GMAIL_USER \
        -e GMAIL_APP_PASSWORD=$GMAIL_APP_PASSWORD \
        -e TO_EMAIL=admin@omgananayaka.in \
        soda-custom:latest \
        python /jobs/scripts/utilities/send_mail.py
        """
    )

    validate_pipeline = BashOperator(
        task_id="validate_pipeline",
        bash_command=f"""
        docker run --rm \
        -v {PROJECT_ROOT}:/jobs \
        soda-custom:latest \
        python /jobs/scripts/quality/validate_pipeline.py
        """
    )

    (
    create_topic
    >> produce_sales
    >> wait_for_stream
    >> load_to_duckdb
    >> soda_scan
    >> notify
    >> validate_pipeline
    )