from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Configuración de SparkSession
spark = SparkSession.builder \
    .appName("KafkaToPostgresRealTime") \
    .master("spark://spark-master:7077").config("spark.jars.packages", "/opt/bitnami/spark/jars/postgresql.jar") \
    .getOrCreate()

# Definir el esquema del JSON que se espera recibir de Kafka
schema = StructType([
    StructField("id", StringType(), True),
    StructField("sensor", StringType(), True),
    StructField("valor", DoubleType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Leer datos de Kafka en tiempo real
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "datos_realtime") \
    .option("startingOffsets", "latest").load()

# Convertir el valor de Kafka (que está en bytes) a String y luego aplicar el esquema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

df = df.withColumn("id", when(col("id").isNull(), "default_id").otherwise(col("id")))

# Función para escribir en PostgreSQL en tiempo real
def write_to_postgres(df, epoch_id):
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/datawarehouse") \
        .option("dbtable", "realtime_data") \
        .option("user", "admin") \
        .option("password", "admin123") \
        .mode("append") \
        .save()

# Escribir el stream en PostgreSQL en tiempo real
query = df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("update") \
    .start()

query.awaitTermination()