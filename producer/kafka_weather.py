# producer/kafka_weather.py
import json
import requests
import time
from kafka import KafkaProducer

API_KEY = "bf56195deaaecbf3ec615eeed7223115"
CITIES = [
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice",
    "Nantes", "Strasbourg", "Montpellier", "Bordeaux",
    "Lille", "Rennes", "Reims", "Saint-Étienne", "Toulon"
]

def send_weather_data():
    producer = KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    topic = "weather_data"

    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},FR&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                print(f"✅ {city} : Données envoyées à Kafka")
                producer.send(topic, data)
            else:
                print(f"❌ Erreur API pour {city} :", data)
        except Exception as e:
            print(f"❌ Erreur pour {city} :", e)

    producer.flush()
    producer.close()
    print("📦 Toutes les données ont été envoyées à Kafka ✅")

# 🔁 Boucle infinie : envoie toutes les 24h
if __name__ == "__main__":
    while True:
        send_weather_data()
        print("⏳ Attente 24h avant le prochain envoi...")
        time.sleep(86400)  # 24h = 86400 secondes