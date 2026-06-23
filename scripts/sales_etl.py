from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
import pyspark.sql.functions as F
from delta import configure_spark_with_delta_pip
import os 

builder = (
    SparkSession.builder
    .appName("sales-order-view")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)


spark = configure_spark_with_delta_pip(builder).getOrCreate()

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