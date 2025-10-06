from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Config PostgreSQL
db_url = "jdbc:postgresql://postgres:5432/weather_db"
db_properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

# Créer session Spark
spark = SparkSession.builder.appName("SparkTest").getOrCreate()

# Exemple simple : dataframe statique pour tester PostgreSQL
data = [("Paris", 20), ("Lyon", 30), ("Marseille", 15)]
columns = ["ville", "temp"]
df = spark.createDataFrame(data, columns)

# Filtrer les villes chaudes (>25°C)
df_hot = df.filter(col("temp") > 25)

# Écrire dans PostgreSQL
df_hot.write.jdbc(db_url, "test_hot", mode="overwrite", properties=db_properties)

spark.stop()
print("Test terminé ✅")
