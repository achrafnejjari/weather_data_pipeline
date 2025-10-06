from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_pipeline')
def run_pipeline():
    try:
        # 1️⃣ Lancer Kafka + récupération API
        subprocess.run(["python", "kafka_producer.py"], check=True)

        # 2️⃣ Lancer Spark pour traiter les données
        subprocess.run(["/opt/spark/bin/spark-submit",
                        "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1",
                        "spark_job.py"], check=True)

        return redirect(url_for('index', status="Pipeline exécuté !"))
    except Exception as e:
        return redirect(url_for('index', status=f"Erreur : {e}"))

if __name__ == '__main__':
    app.run(debug=True)
