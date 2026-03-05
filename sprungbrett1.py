import streamlit as st
import google.generativeai as genai

# UI Konfiguration
st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Sprungbrett-Labor")

st.info("Schritt 1: App-Oberfläche geladen. Wir testen jetzt die Leitung.")

# 1. Key aus den Secrets ziehen
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.write("✅ API-Schlüssel wurde im System gefunden.")
else:
    st.error("❌ Fehler: GOOGLE_API_KEY fehlt in den Secrets!")
    st.stop()

# 2. Manueller Verbindungstest
if st.button("Verbindung zum Pro-Server testen"):
    try:
        # Wir nutzen gemini-1.5-flash, da es im Billing-Projekt aktiv ist
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        with st.spinner('Anfrage an Google wird gesendet...'):
            response = model.generate_content("Antworte mit 'OK'")
            
        if response:
            st.success(f"🚀 Erfolg! Die KI sagt: {response.text}")
            st.balloons()
    except Exception as e:
        st.error(f"Stolperstein: {e}")
        st.info("Tipp: Wenn hier 404 steht, prüfen wir als nächstes die API-Version.")
