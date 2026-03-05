import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Sprungbrett-Labor")

st.info("Schritt 3: Wir nutzen jetzt das Modell 'gemini-2.5-flash' aus deiner Liste.")

# 1. Key laden
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt!")
    st.stop()

# 2. Verbindungstest mit dem RICHTIGEN Modell
if st.button("Pro-Verbindung mit Gemini 2.5 testen"):
    try:
        # Wir nutzen EXAKT den Namen aus deiner Liste
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        with st.spinner('Signal wird an den 2026er Pro-Server gesendet...'):
            response = model.generate_content("Antworte mit: 'Verbindung erfolgreich, Zwi!'")
            
        if response.text:
            st.success(f"✅ Volltreffer! Die KI sagt: {response.text}")
            st.balloons()
            st.session_state.connected = True
    except Exception as e:
        st.error(f"Fehler: {e}")
        st.info("Falls hier wieder v1beta steht, ist die Google-Bibliothek in Streamlit veraltet.")

# 3. Ausblick
if st.session_state.get("connected"):
    st.write("---")
    st.write("### Nächster Schritt für Jennifer")
    st.write("Die Leitung steht! Soll ich jetzt die Logik für die Energiefresser einbauen?")
