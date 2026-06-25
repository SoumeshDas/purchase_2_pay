import os
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

BOOTSTRAP_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
TOPIC_NAME = "sales_topic"

print(f"Connecting to Kafka: {BOOTSTRAP_SERVER}")

admin_client = KafkaAdminClient(
    bootstrap_servers=BOOTSTRAP_SERVER,
    client_id="purchase2pay-admin"
)

topic = NewTopic(
    name=TOPIC_NAME,
    num_partitions=1,
    replication_factor=1
)

try:
    admin_client.create_topics(
        new_topics=[topic],
        validate_only=False
    )
    print(f"✅ Topic '{TOPIC_NAME}' created successfully.")

except TopicAlreadyExistsError:
    print(f"ℹ️ Topic '{TOPIC_NAME}' already exists.")

finally:
    admin_client.close()