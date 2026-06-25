from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="purchase_2_pay_pipeline",
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
) as dag:

    create_topic = BashOperator(
        task_id="create_topic",
        bash_command="python /jobs/scripts/create_sales_topic.py"
    )

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

    run_spark = BashOperator(
        task_id="run_spark",
        bash_command="""
        docker exec -i spark-master \
        /opt/spark/bin/spark-submit \
        --master spark://spark-master:7077 \
        /jobs/scripts/sales_etl.py
        """
    )

    create_topic >> produce_sales >> run_spark