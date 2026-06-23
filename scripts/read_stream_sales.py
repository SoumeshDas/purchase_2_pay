from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SalesReader")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

df = spark.read.parquet("/jobs/output/sales_stream")

print("Count =", df.count())

df.printSchema()

df.show(truncate=False)