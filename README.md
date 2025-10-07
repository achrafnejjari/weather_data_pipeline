# 🌤️ Weather Data Pipeline – Kafka + PostgreSQL + Streamlit

Un pipeline de données en temps réel qui collecte les données météorologiques via l’API OpenWeatherMap, les transmet via **Apache Kafka**, les stocke dans **PostgreSQL**, et les visualise dans un **dashboard interactif Streamlit**.

---

## 🚀 Fonctionnalités

- **Producer** : Récupère la météo de 14 villes françaises toutes les 24h via OpenWeatherMap → envoie à Kafka
- **Consumer** : Lit les messages Kafka → stocke dans PostgreSQL (une ligne par ville, mise à jour automatique)
- **Dashboard** : Interface Streamlit avec graphiques interactifs, filtres et export CSV
- **Monitoring** : pgAdmin intégré pour explorer les données
- **CI/CD** : Validation automatique via GitHub Actions 

---

## 🏗️ Architecture

```mermaid
graph LR
A[OpenWeatherMap API] --> B(Producer)
B --> C{Apache Kafka}
C --> D(Consumer)
D --> E[(PostgreSQL)]
E --> F[Streamlit Dashboard]
E --> G[pgAdmin]
