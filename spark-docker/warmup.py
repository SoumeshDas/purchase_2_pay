from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("dependency-cache")
    .getOrCreate()
)

print("Kafka dependencies downloaded successfully.")

spark.stop()