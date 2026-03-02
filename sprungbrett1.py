import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett-Chat", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# API Key sicher laden
api_key = st.sidebar.text_input("API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Chat-Historie in Streamlit initialisieren
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

        # Antwort von Gemini generieren
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Wir übergeben die gesamte Historie für den Dialog-Kontext
        chat = model.start_chat(history=[
            {"role": m["role"] == "user" and "user" or "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("Bitte gib den API-Key ein, um den Dialog zu starten.")