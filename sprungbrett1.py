import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# API Key sicher aus den Streamlit Secrets laden
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Bitte hinterlege den 'GOOGLE_API_KEY' in den Streamlit-Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Die System Instruction - Fokus auf 1. Halbjahr 2026
# Wir setzen hier die Ziele für Respekt, Wertschätzung und Motivation um [cite: 31, 32]
system_instruction = """
Du bist der pragmatische Impuls-Geber für das Führungslabor. 
STRIKTER DIALOG-ABLAUF:
1. Der User startet mit "Hallo".
2. Du fragst: "Welcher Energiefresser beschäftigt dich heute?"
3. Danach fragst du: "Wähle dein Sprungbrett: 1m (leicht), 3m (mutig) oder 5m (Herausforderung)?"
4. Dann gibst du die REZEPTKARTE aus:
   - AKTION: (kurz & knackig)
   - REFLEXIONSFRAGE: (für den Feierabend)
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
        # Geänderter Modellname für maximale Kompatibilität in 2026
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=system_instruction
        )
        
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        with st.spinner('Verbindung zum Führungslabor wird aufgebaut...'):
            response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # Falls 'gemini-1.5-flash' immer noch zickt, versuchen wir die aktuellste Version
        st.warning("Versuche alternative Verbindung...")
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", system_instruction=system_instruction)
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.chat_message("assistant").markdown(response.text)
        except:
            st.error(f"Kritischer Fehler: {e}")

if st.sidebar.button("Dialog neu starten"):
    st.session_state.messages = []
    st.rerun()
