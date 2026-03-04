import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# 1. Sicherstellen, dass der Key da ist
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API-Key fehlt in den Secrets!")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # System-Anweisung
    instruction = "Du bist der Sprungbrett-Generator. Start: Hallo. Dann Frage nach Energiefresser. Dann Frage nach 1m, 3m, 5m. Dann Aktion & Reflexion."

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat anzeigen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Schreibe 'Hallo'..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Stabiler Modell-Aufruf
        # Wir nutzen 'gemini-1.5-flash', das ist am verlässlichsten
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=instruction
        )
        
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        with st.spinner('Verbindung wird aufgebaut...'):
            # Hier passiert oft der Fehler - wir fangen ihn ab
            response = chat.send_message(prompt)
            
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    # Das verhindert das "Zurückspringen" und zeigt dir, was genau schief läuft
    st.error(f"Ein technischer Fehler ist aufgetreten: {e}")
    st.info("Prüfe, ob dein API-Key im Google AI Studio noch aktiv ist.")

if st.sidebar.button("Reset"):
    st.session_state.messages = []
    st.rerun()
