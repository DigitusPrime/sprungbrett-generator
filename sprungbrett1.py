import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# API Key aus Secrets laden
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Fehler: GOOGLE_API_KEY in Streamlit Secrets nicht gefunden.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Die System Instruction für den Dialog
system_instruction = """
Du bist der Impuls-Geber für das Führungslabor. Dein Ziel ist Bewegung im System[cite: 38].
DIALGO-REGELN:
1. Start: "Hallo".
2. Frage: "Welcher Energiefresser beschäftigt dich heute?" 
3. Nach Antwort: Frage nach Sprungbrett-Höhe (1m, 3m, 5m).
4. Finale: Gib AKTION und REFLEXIONSFRAGE aus. Fokus: Lösungsorientierung und Teamkraft[cite: 27].
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
        # Hier nutzen wir den exakten Modell-String
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash", 
            system_instruction=system_instruction
        )
        
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        with st.spinner('Überlege...'):
            response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"KI-Verbindung fehlgeschlagen. Bitte prüfe dein Google AI Studio Projekt. Details: {e}")

if st.sidebar.button("Dialog neu starten"):
    st.session_state.messages = []
    st.rerun()
