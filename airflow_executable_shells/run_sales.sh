#!/bin/bash

/opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --total-executor-cores 1 \
  --executor-memory 512m \
  /jobs/scripts/test_cluster.py