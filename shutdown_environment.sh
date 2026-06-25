#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Stopping Spark..."
cd "$PROJECT_ROOT/spark-docker"
docker compose down

echo "Stopping Kafka..."
cd "$PROJECT_ROOT/kafka-docker"
docker compose down

echo "Environment stopped."