#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "========================================="
echo " Purchase2Pay Environment Setup"
echo "========================================="

#####################################################
# Start Kafka
#####################################################

echo "Starting Kafka..."
cd "$PROJECT_ROOT/kafka-docker"
docker compose up -d

#####################################################
# Wait for Kafka
#####################################################

echo ""
echo "Waiting for Kafka..."

docker run --rm \
  --network kafka-docker_default \
  -e KAFKA_SERVER=kafka:9092 \
  -v "$PROJECT_ROOT":/jobs \
  kafka-python-docker:1.0 \
  python /jobs/scripts/utilities/wait_for_kafka.py

echo "Kafka is ready."

#####################################################
# Create Topic
#####################################################

echo ""
echo "Creating Kafka Topic..."

docker run --rm \
  --network kafka-docker_default \
  -e KAFKA_SERVER=kafka:9092 \
  -v "$PROJECT_ROOT":/jobs \
  kafka-python-docker:1.0 \
  python /jobs/scripts/utilities/create_sales_topic.py

#####################################################
# Start Spark
#####################################################

echo ""
echo "Starting Spark..."

cd "$PROJECT_ROOT/spark-docker"
docker compose up -d

echo ""
echo "========================================="
echo " Environment Ready"
echo "========================================="