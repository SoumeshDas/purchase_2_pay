# test_cluster.py

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("cluster-test").getOrCreate()

df = spark.range(10)

df.show()

spark.stop()
