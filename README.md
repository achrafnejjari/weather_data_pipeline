# 🌤️ Weather Data Pipeline – Kafka + PostgreSQL + Streamlit

Un pipeline de données en temps réel qui collecte les données météorologiques via l’API OpenWeatherMap, les transmet via **Apache Kafka (broker + topic)**, les stocke dans **PostgreSQL**, et les visualise dans un **dashboard interactif Streamlit** avec **graphiques Plotly**.

---

## 🚀 Fonctionnalités

- **Producer** : Script Python qui récupère la météo de 14 villes françaises via **OpenWeatherMap API** et envoie les données à Kafka
- **Kafka** : Utilisation d’un **broker Kafka** et d’un **topic** (`weather_data`) pour le streaming des messages
- **Consumer** : Script Python qui lit les messages depuis Kafka et stocke les données dans **PostgreSQL** (une ligne par ville, mise à jour automatique)
- **Dashboard** : Interface **Streamlit** avec visualisations interactives (**Plotly**), filtres dynamiques et export CSV
- **Monitoring** : **pgAdmin** intégré pour explorer et requêter la base de données
- **CI** : Validation automatique via **GitHub Actions** (build Docker, vérification syntaxe Python)

---

## 🏗️ Architecture

```mermaid
graph LR
A[OpenWeatherMap API] --> B(Producer Python)
B --> C{Kafka Broker<br><small>Topic: weather_data</small>}
C --> D(Consumer Python)
D --> E[(PostgreSQL)]
E --> F[Streamlit + Plotly]
E --> G[pgAdmin]
