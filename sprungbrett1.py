import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Sprungbrett Diagnose & Chat")

# 1. Key laden
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"].replace("[", "").replace("]", "").strip()
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt!")
    st.stop()

# 2. DIAGNOSE: Was ist wirklich verfügbar?
with st.expander("🔍 System-Check (Klick mich bei Fehlern)"):
    try:
        # Wir listen alle verfügbaren Modelle auf
        available_models = [m.name for m in genai.list_models()]
        st.write("Dein Key hat Zugriff auf:", available_models)
    except Exception as e:
        st.error(f"Diagnose fehlgeschlagen: {e}")

# 3. CHAT-LOGIK
# Wir probieren das stabilste 2026er Modell: gemini-2.5-flash
# Falls das in deiner Region nicht geht, nimm gemini-3-flash-preview
MODEL_ID = "gemini-2.5-flash" 

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
        # WICHTIG: Wir nutzen die GenerativeModel Klasse OHNE Beta-Parameter
        model = genai.GenerativeModel(MODEL_ID)
        
        # Einfacher Prompt-Aufruf (keine History-Komplexität für den Test)
        response = model.generate_content(
            f"Du bist der Sprungbrett-Generator. Antworte auf: {prompt}"
        )
        
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Fehler mit {MODEL_ID}: {e}")
        st.info("Versuche in der Diagnose-Liste oben ein Modell zu finden, das 'generateContent' unterstützt.")
