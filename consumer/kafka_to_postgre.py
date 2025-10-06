# kafka_to_postgre.py
import json
import psycopg2
from kafka import KafkaConsumer
import time

# Configuration
KAFKA_TOPIC = "weather_data"
KAFKA_SERVER = "kafka:9092"
POSTGRES_HOST = "postgres"
POSTGRES_DB = "weather_db"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

def get_db_connection():
    """Crée une connexion à PostgreSQL"""
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def create_table():
    """Crée la table weather avec clé primaire et timestamp"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                city VARCHAR(100) PRIMARY KEY,
                temperature FLOAT,
                humidity INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        print("✅ Table 'weather' prête (clé primaire sur 'city').")
    except Exception as e:
        print(f"❌ Erreur création table : {e}")
    finally:
        if conn:
            conn.close()

def main():
    # Créer la table au démarrage
    create_table()

    # Démarrer le consumer Kafka
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='weather-group'
    )

    print("✅ En attente de messages Kafka...")

    for message in consumer:
        data = message.value
        try:
            city = data.get("name")
            temp = data.get("main", {}).get("temp")
            humidity = data.get("main", {}).get("humidity")

            if city and temp is not None and humidity is not None:
                conn = None
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO weather (city, temperature, humidity)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (city) DO UPDATE SET
                            temperature = EXCLUDED.temperature,
                            humidity = EXCLUDED.humidity,
                            updated_at = CURRENT_TIMESTAMP
                    """, (city, temp, humidity))
                    conn.commit()
                    cur.close()
                    print(f"✅ Mis à jour : {city} | {temp}°C | {humidity}%")
                except Exception as db_error:
                    print(f"❌ Erreur DB : {db_error}")
                finally:
                    if conn:
                        conn.close()
            else:
                print("❌ Données incomplètes :", data)
        except Exception as e:
            print(f"❌ Erreur traitement message : {e}")

if __name__ == "__main__":
    # Attente pour que Kafka soit prêt (optionnel mais utile)
    print("⏳ Attente 10s pour que Kafka démarre...")
    time.sleep(10)
    main()