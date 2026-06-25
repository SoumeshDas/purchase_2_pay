#!/bin/bash

# Get the absolute path of the project root
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "========================================="
echo " Purchase2Pay Environment Setup"
echo "========================================="

echo "Starting Kafka..."
cd "$PROJECT_ROOT/kafka-docker"
docker compose up -d

echo "Creating Kafka topic..."
docker run --rm \
  --network kafka-docker_default \
  -e KAFKA_SERVER=kafka:9092 \
  -v "$PROJECT_ROOT":/jobs \
  kafka-python-docker:1.0 \
  python /jobs/scripts/create_sales_topic.py

echo "Starting Spark..."
cd "$PROJECT_ROOT/spark-docker"
docker compose up -d

echo ""
echo "========================================="
echo " Environment Ready"
echo "========================================="