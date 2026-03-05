import streamlit as st
import google.generativeai as genai

# Grundkonfiguration (Muss ganz oben stehen)
st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")

# Sofortige Anzeige, damit das Rädchen aufhört zu drehen
st.title("🚀 Sprungbrett-Labor")
st.write("Status: App gestartet. Warte auf Eingabe...")

# 1. Key-Check
if "GOOGLE_API_KEY" in st.secrets:
    # Wir reinigen den Key extrem vorsichtig
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Kein API-Key in den Secrets gefunden!")
    st.stop()

# 2. Einfacher Test-Dialog
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.chat_input("Schreibe 'Hallo'...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Wir nutzen gemini-1.5-flash, das ist der stabilste Standard
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        with st.spinner('Verbindung zum Pro-Server wird aufgebaut...'):
            # Wir packen die Anweisung direkt in den Aufruf
            response = model.generate_content(
                f"Du bist der Sprungbrett-Generator. Antworte kurz auf: {prompt}"
            )
            
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.balloons() # Ein kleines Erfolgserlebnis!
    except Exception as e:
        st.error(f"Technisches Detail: {e}")
        st.info("Tipp: Wenn hier 404 steht, ist die API im Google Projekt noch nicht bereit.")

# Knopf zum Zurücksetzen in der Seitenleiste
if st.sidebar.button("App neu starten"):
    st.session_state.chat_history = []
    st.rerun()
