# spark_kafka_to_postgres.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

spark = SparkSession.builder \
    .appName("WeatherKafkaToPostgres") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

# Schéma des données météo
schema = StructType([
    StructField("name", StringType(), True),
    StructField("main", StructType([
        StructField("temp", FloatType(), True),
        StructField("humidity", IntegerType(), True)
    ])),
    StructField("dt", IntegerType(), True)
])

# Lire depuis Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather_data") \
    .load()

# Parser le JSON
weather_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select(
    col("data.name").alias("city"),
    col("data.main.temp").alias("temperature"),
    col("data.main.humidity").alias("humidity")
)

# Écrire dans PostgreSQL (en mode batch ou streaming avec foreachBatch)
def write_to_postgres(df, epoch_id):
    df.write \
      .format("jdbc") \
      .option("url", "jdbc:postgresql://postgres:5432/weather_db") \
      .option("dbtable", "weather") \
      .option("user", "postgres") \
      .option("password", "postgres") \
      .option("driver", "org.postgresql.Driver") \
      .mode("append") \
      .save()

query = weather_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()