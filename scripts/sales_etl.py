from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os

spark = (
    SparkSession.builder
    .appName("sales-order-view")
    .getOrCreate()
)

#project_path = "/home/soumeshchnandradas/source_code/airflow_spark_test_project"
project_path = "/jobs"

read_file_path = os.path.join(project_path, "data", "Sales_csv.csv")
output_file_path = os.path.join(project_path, "output", "customer_sales")

df = spark.read.csv(read_file_path,header = True,inferSchema = True)
df = df.withColumn(
    "Quantity",
    F.expr("try_cast(Quantity as double)")
)

print("Input_Data")
df.show()

print("change the column name ")

df = df.toDF(*[
    c.lower().replace(" ", "_")
    for c in df.columns
])

result = df.groupBy("customer_name").agg(F.sum(F.col("quantity")).alias("per_customer_sales_quantity"))

print("Aggregated Results")
result.show()

print("write the files")
result.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(output_file_path)


spark.stop()