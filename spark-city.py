from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

from config import configuration  # External config file with AWS keys & bootstrap server

# ==================== Spark App Start ====================
spark = SparkSession.builder.appName("SmartCityKafkaToS3") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
            "org.apache.hadoop:hadoop-aws:3.3.1,"
            "com.amazonaws:aws-java-sdk:1.11.469") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", configuration['AWS_ACCESS_KEY']) \
    .config("spark.hadoop.fs.s3a.secret.key", configuration['AWS_SECRET_KEY']) \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# ==================== Define Schemas ====================
vehicleSchema = StructType([
    StructField("id", StringType(), True),
    StructField("deviceID", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("elevation", DoubleType(), True),
    StructField("speed", DoubleType(), True),
    StructField("length", DoubleType(), True)
])

weatherSchema = StructType([
    StructField("id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("weatherCondition", StringType(), True),
    StructField("windSpeed", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("airQualityIndex", DoubleType(), True)
])

failureSchema = StructType([
    StructField("id", StringType(), True),
    StructField("deviceID", StringType(), True),
    StructField("incidentId", StringType(), True),
    StructField("type", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("location", StructType([
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True)
    ]), True),
    StructField("description", StringType(), True),
    StructField("num_failures", DoubleType(), True)
])

# ==================== Read Kafka Helper ====================
def read_kafka(topic, schema):
    return (spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", configuration['KAFKA_BOOTSTRAP_SERVERS'])
            .option("subscribe", topic)
            .option("startingOffsets", "earliest")
            .option("failOnDataLoss", "false")
            .load()
            .selectExpr("CAST(value AS STRING)")
            .select(from_json(col("value"), schema).alias("data"))
            .select("data.*")
            .withColumn("parsed_timestamp", col("timestamp").cast(TimestampType()))
            .withWatermark("parsed_timestamp", "2 minutes"))

# ==================== Write Stream Helper ====================
def write_parquet(df, table_name):
    return (df.writeStream
            .format("parquet")
            .outputMode("append")
            .option("path", f"s3a://sparkstreamingdata/data/{table_name}")
            .option("checkpointLocation", f"s3a://sparkstreamingdata/checkpoints/{table_name}")
            .start())

# ==================== Ingest Streams ====================
vehicle_df = read_kafka("vehicle_data", vehicleSchema)
weather_df = read_kafka("weather_data", weatherSchema)
failure_df = read_kafka("failure_data", failureSchema)

# ==================== Write to S3 ====================
vehicle_query = write_parquet(vehicle_df, "vehicle_data")
weather_query = write_parquet(weather_df, "weather_data")
failure_query = write_parquet(failure_df, "failure_data")

# ==================== Await Termination ====================
spark.streams.awaitAnyTermination()
