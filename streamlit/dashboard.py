import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px 
from datetime import datetime

# ----------------------------
# Configuration de la page
# ----------------------------
st.set_page_config(
    page_title="🌦️ Dashboard Météo France",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Fonction pour créer une connexion TEMPORAIRE
# ----------------------------
def get_db_connection():
    return psycopg2.connect(
        host="postgres",
        database="weather_db",
        user="postgres",
        password="postgres"
    )

# ----------------------------
# Chargement des données (avec connexion temporaire)
# ----------------------------
@st.cache_data(ttl=60)  # Rafraîchit toutes les 60s
def load_data():
    conn = None
    try:
        conn = get_db_connection()
        query = """
        SELECT 
            city,
            temperature,
            humidity,
            updated_at
        FROM weather
        ORDER BY temperature DESC
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        if conn:
            conn.close()  # ← Ferme toujours la connexion

# ----------------------------
# Interface utilisateur
# ----------------------------
st.title("🌦️ Dashboard Météo en Temps Réel - France")
st.markdown("Données actualisées automatiquement toutes les minutes.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    st.markdown("### Dernière mise à jour")
    st.write(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    if st.button("🔄 Rafraîchir maintenant"):
        st.cache_data.clear()
        st.rerun()

# Charger les données
df = load_data()

if df.empty:
    st.warning("⚠️ Aucune donnée disponible. Le producer a-t-il envoyé des données ?")
else:
    # ----------------------------
    # Métriques principales
    # ----------------------------
    col1, col2, col3 = st.columns(3)
    
    avg_temp = df['temperature'].mean()
    max_temp = df['temperature'].max()
    min_temp = df['temperature'].min()
    
    col1.metric("🌡️ Température moyenne", f"{avg_temp:.1f}°C")
    col2.metric("🔥 Température max", f"{max_temp:.1f}°C")
    col3.metric("❄️ Température min", f"{min_temp:.1f}°C")

    # ----------------------------
    # Graphiques
    # ----------------------------
    st.subheader("📊 Visualisation des données")

    # Température par ville
    fig_temp = px.bar(
        df,
        x='city',
        y='temperature',
        color='temperature',
        color_continuous_scale='RdYlBu_r',
        title="Température par ville",
        labels={'temperature': 'Température (°C)', 'city': 'Ville'}
    )
    fig_temp.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_temp, use_container_width=True)

    # Humidité vs Température
    fig_scatter = px.scatter(
        df,
        x='temperature',
        y='humidity',
        size='temperature',
        color='city',
        hover_name='city',
        title="Relation Température / Humidité",
        labels={
            'temperature': 'Température (°C)',
            'humidity': 'Humidité (%)'
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ----------------------------
    # Tableau de données
    # ----------------------------
    st.subheader("📋 Données brutes")
    
    # Filtres
    st.markdown("### 🔍 Filtres")
    min_temp_filter = st.slider("Température minimale", 
                               float(df['temperature'].min()), 
                               float(df['temperature'].max()), 
                               float(df['temperature'].min()))
    
    filtered_df = df[df['temperature'] >= min_temp_filter]
    
    # Tableau stylisé
    st.dataframe(
        filtered_df.style.background_gradient(
            subset=['temperature'], 
            cmap='coolwarm'
        ).format({
            'temperature': '{:.1f}°C',
            'humidity': '{}%',
            'updated_at': lambda x: x.strftime('%d/%m %H:%M')  # ← format lisible
        }),
        use_container_width=True,
        height=400
    )

    # ----------------------------
    # Export
    # ----------------------------
    st.subheader("📥 Export des données")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Télécharger en CSV",
        data=csv,
        file_name=f"meteo_france_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

# ----------------------------
# Pied de page
# ----------------------------
st.markdown("---")
st.caption("© 2025 - Pipeline Météo Kafka | Données OpenWeatherMap")