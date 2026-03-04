import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# API Key sicher laden
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Fehler: GOOGLE_API_KEY fehlt in den Streamlit-Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# System Instruction - Fokus 2026: Energiefresser & Teamkraft
system_instruction = """
Du bist der Sprungbrett-Generator für das Führungslabor.
DEIN ABLAUF:
1. Auf "Hallo" antwortest du: "Hallo! Welcher Energiefresser nervt dich heute?"
2. Nach der Antwort fragst du nach dem Brett: 1m (leicht), 3m (mutig) oder 5m (Challenge).
3. Dann gibst du die REZEPTKARTE aus (Aktion & Reflexionsfrage).
Fokus: Wertschätzung, Selbstschutz und Klarheit im FM-Alltag.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Schreibe 'Hallo' um zu starten..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Wir nutzen EXAKT den Namen aus deinem AI Studio Screenshot
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview", 
            system_instruction=system_instruction
        )
        
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        with st.spinner('Verbindung steht...'):
            response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Technischer Stolperstein: {str(e)}")
        st.info("Prüfe im AI Studio, ob der API-Key unter 'Sprungbrett ZHAW' noch aktiv ist.")

if st.sidebar.button("Dialog neu starten"):
    st.session_state.messages = []
    st.rerun()
