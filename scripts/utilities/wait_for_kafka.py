import os
import sys
import time
from kafka import KafkaAdminClient

BOOTSTRAP_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

while True:
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=BOOTSTRAP_SERVER,
            request_timeout_ms=3000,
        )
        admin.list_topics()
        admin.close()

        print("✅ Kafka is Ready")
        sys.exit(0)

    except Exception as e:
        print(f"Waiting for Kafka... ({e})")
        time.sleep(2)