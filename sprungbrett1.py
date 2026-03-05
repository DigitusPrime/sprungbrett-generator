import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# 1. Key extrem sicher laden und säubern
if "GOOGLE_API_KEY" in st.secrets:
    raw_key = st.secrets["GOOGLE_API_KEY"]
    # Entfernt alle möglichen Sonderzeichen wie [ ] " oder Leerzeichen
    api_key = raw_key.replace("[", "").replace("]", "").replace('"', "").strip()
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Secrets!")
    st.stop()

# 2. Die Instruktion für das Führungslabor 2026
instruction = "Handle als Coach. Ablauf: 1. Frage nach Energiefresser. 2. Frage nach 1m, 3m, 5m. 3. Gib Aktion & Reflexionsfrage aus."

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
        # 3. Stabiler Aufruf über das GenerativeModel
        # Wir verzichten auf system_instruction im Konstruktor, da dies den v1beta-Fehler auslöst!
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Wir bauen den Kontext manuell zusammen
        full_prompt = f"System-Anweisung: {instruction}\n\nNutzer: {prompt}"
        
        with st.spinner('Führungslabor wird verbunden...'):
            response = model.generate_content(full_prompt)
            
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            st.warning("Die KI hat keine Antwort geliefert. Prüfe dein Billing-Guthaben.")

    except Exception as e:
        st.error(f"Technisches Detail: {e}")
