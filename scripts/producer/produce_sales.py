import os
from kafka import KafkaProducer
import json
import time

BOOTSTRAP_SERVER = os.getenv("KAFKA_SERVER", "localhost:29092")
print(f"Connecting to Kafka: {BOOTSTRAP_SERVER}")
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

for i in range(1, 101):
    record = {"customer": f"Customer_{i % 3}", "quantity": i * 10}

    producer.send("sales_topic", record)
    print(record)
    time.sleep(1)

producer.flush()
