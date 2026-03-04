import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API-Key fehlt in den Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Wir packen die Anweisung direkt in den ersten Prompt, 
# falls der Beta-Kanal mit System Instructions zickt.
instruction = """
Du bist der Sprungbrett-Generator für das Führungslabor 2026.
ABLAUF: 
1. Frag nach dem Energiefresser.
2. Frag nach 1m, 3m oder 5m.
3. Gib Aktion & Reflexion aus.
"""

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
        # KORREKTUR: Wir nutzen das stabilste Modell ohne 'models/' Präfix
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # Wir übergeben die Instruktion hier als Teil des Kontexts
        chat = model.start_chat(history=[
            {"role": "user", "parts": [instruction]},
            {"role": "model", "parts": ["Verstanden. Ich bin bereit."]}
        ])
        
        # Den bisherigen Chat-Verlauf hinzufügen
        for m in st.session_state.messages[:-1]:
            chat.history.append({"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]})

        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Verbindungsproblem: {e}")
        st.info("Tipp: Prüfe, ob im Google Cloud Billing die Abrechnung wirklich aktiv ist.")

if st.sidebar.button("Reset"):
    st.session_state.messages = []
    st.rerun()
