FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka_weather.py .

# "Quand tu lances le conteneur, exécute cette commande" :
CMD ["python", "kafka_weather.py"]  