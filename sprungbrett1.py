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

# Die System Instruction für das Führungslabor 2026
system_instruction = """
Du bist der interaktive „Sprungbrett-Generator“. 
ABLAUF:
1. Start: "Hallo".
2. Frage nach dem Energiefresser (Fokus: 1. Halbjahr 2026).
3. Frage nach der Höhe: 1m (leicht), 3m (mutig), 5m (Herausforderung).
4. Gib eine AKTION und eine REFLEXIONSFRAGE aus.
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

    # Wir probieren verschiedene Modellnamen, falls einer nicht gefunden wird
    model_names = ["gemini-1.5-flash", "gemini-3-flash-preview", "models/gemini-1.5-flash"]
    response_text = ""
    
    for m_name in model_names:
        try:
            model = genai.GenerativeModel(model_name=m_name, system_instruction=system_instruction)
            chat = model.start_chat(history=[
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            response_text = response.text
            break # Wenn es klappt, brechen wir die Suche ab
        except Exception:
            continue
    
    if response_text:
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:
        st.error("Verbindung zur KI fehlgeschlagen. Bitte prüfe, ob dein API-Key im AI Studio noch aktiv ist.")

if st.sidebar.button("Dialog neu starten"):
    st.session_state.messages = []
    st.rerun()
