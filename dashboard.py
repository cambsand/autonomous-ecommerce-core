import sqlite3
import subprocess
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Autonomous E-Commerce Core", layout="wide")
st.title("🛒 E-Commerce Autonomous Control Center")

# Sidebar - Azioni rapide
st.sidebar.header("Pannello di Controllo")
if st.sidebar.button("🚀 Esegui Pipeline Ora"):
    with st.spinner("Esecuzione della pipeline in corso..."):
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        st.sidebar.success("Pipeline completata!")
        st.sidebar.text_area("Output Log", result.stdout, height=150)

# Vista Catalogo dal DB SQLite
st.header("📊 Prodotti e Trend Salvati")

try:
    conn = sqlite3.connect("data/ecommerce_core.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()

    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Totale Prodotti Inseriti", len(df))
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nessun dato presente nel database. Clicca su 'Esegui Pipeline Ora' per iniziare.")
except Exception as e:
    st.warning("Database non ancora inizializzato o vuoto.")