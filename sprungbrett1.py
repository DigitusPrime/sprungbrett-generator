import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# WICHTIG: Hast du den neuen Key (...u0QA) in Streamlit Secrets kopiert?
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Bitte hinterlege den neuen Key (...u0QA) in den Streamlit-Secrets!")
    st.stop()

# Die Instruktion für den Ablauf
instruction = """Du bist der Sprungbrett-Generator für das Führungslabor. 
REGEKLN: Auf 'Hallo' fragst du nach dem Energiefresser. 
Dann fragst du nach 1m, 3m oder 5m. 
Am Ende gibst du AKTION und REFLEXIONSFRAGE aus."""

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
        # Wir verzichten auf 'system_instruction' im Modell-Aufruf,
        # um den v1beta-Fehler komplett zu umgehen.
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Wir bauen die Anweisung direkt in den Kontext ein
        full_prompt = f"Anweisung: {instruction}\n\nNutzer: {prompt}"
        
        with st.spinner('Verbindung wird stabilisiert...'):
            response = model.generate_content(full_prompt)
            
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Verbindungsproblem: {e}")
        st.info("Tipp: Prüfe, ob der Key u0QA wirklich in den Streamlit Secrets steht.")
