import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API-Key fehlt!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Kurz & knapp für maximale Stabilität
instruction = "Du bist der Sprungbrett-Generator. Prozess: Hallo -> Welcher Energiefresser? -> 1m, 3m oder 5m? -> Aktion & Reflexion."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Schreibe 'Hallo'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # WICHTIG: Nur der Name, ohne "models/" Präfix
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=instruction
        )
        
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # Wenn Flash nicht geht, probieren wir das Pro-Modell als Backup
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=instruction)
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except:
            st.error(f"Technischer Fehler: {e}")

if st.sidebar.button("Reset"):
    st.session_state.messages = []
    st.rerun()
