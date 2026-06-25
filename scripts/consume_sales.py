from pyspark.sql import SparkSession
from pyspark.sql.functions import col,from_json
from pyspark.sql.types import StructType,StringType,IntegerType

spark = (
    SparkSession.builder
    .appName("KafkaSalesConsumer")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "sales_topic")
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
)

schema = StructType() \
    .add("customer", StringType()) \
    .add("quantity", IntegerType())

json_df = df.selectExpr("CAST(value AS STRING) as json_string")

parsed_df = json_df.select(
    from_json(col("json_string"), schema).alias("data")
).select("data.*")


query = (
    parsed_df.writeStream
    .outputMode("append")
    .format("parquet")
    .option("path", "/jobs/output/sales_stream")
    .option("checkpointLocation", "/jobs/checkpoints/sales_stream")
    .start()
)

query.awaitTermination()