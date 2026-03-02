import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="FM Sprungbrett-Chat", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# API Key automatisch aus den Streamlit Secrets laden
# WICHTIG: Der Name in den Secrets muss exakt "GOOGLE_API_KEY" sein
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Chat-Historie initialisieren
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Historie anzeigen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Nutzer-Eingabe
    if prompt := st.chat_input("Schreibe 'Hallo' um zu starten..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Antwort generieren (Fokus auf Ziele 2026: Energiefresser & Wertschätzung)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Dialog-Kontext aufbauen
        chat = model.start_chat(history=[
            {"role": m["role"] == "user" and "user" or "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        with st.spinner('Überlege...'):
            response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

else:
    st.error("API Key fehlt! Bitte hinterlege 'GOOGLE_API_KEY' in den Streamlit Cloud Secrets.")
