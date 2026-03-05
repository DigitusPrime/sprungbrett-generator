import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Sprungbrett-Labor")

st.info("Schritt 2: Wir testen jetzt die stabile Pro-Leitung.")

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
    # WICHTIG: Wir konfigurieren hier NUR den Key
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt!")
    st.stop()

# Wir bauen eine Diagnose-Funktion ein
if st.button("Verfügbare Modelle auflisten"):
    try:
        models = [m.name for m in genai.list_models()]
        st.write("Dein Key sieht folgende Modelle:", models)
    except Exception as e:
        st.error(f"Diagnose fehlgeschlagen: {e}")

if st.button("Stabile Verbindung testen"):
    try:
        # TRICK: Wir nutzen hier 'gemini-1.5-flash-latest'
        # Dieser Name erzwingt oft den stabilen v1-Kanal
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        with st.spinner('Sende Signal an Pro-Server...'):
            response = model.generate_content("Antworte mit: 'Leitung steht!'")
            
        if response.text:
            st.success(f"✅ Volltreffer! Die KI sagt: {response.text}")
            st.balloons()
    except Exception as e:
        st.error(f"Immer noch v1beta-Fehler? Details: {e}")
        st.info("Falls es nicht geht: Klicke oben auf 'Modelle auflisten' und sag mir, was dort steht.")
