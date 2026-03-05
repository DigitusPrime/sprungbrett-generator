import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# 1. Key laden (ohne Umwege)
if "GOOGLE_API_KEY" in st.secrets:
    # Wir bereinigen den Key von eventuellen Leerzeichen
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip('[')
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Streamlit-Secrets!")
    st.stop()

# 2. Instruktion (In den Chat eingebaut statt als System-Modus)
instruction = """
Handle als Coach für das Führungslabor. 
Ablauf: 
1. Auf 'Hallo' fragst du: 'Welcher Energiefresser beschäftigt dich heute?' 
2. Dann fragst du nach der Sprungbretthöhe (1m, 3m, 5m). 
3. Dann gibst du AKTION und REFLEXIONSFRAGE aus.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nutzer-Eingabe
if prompt := st.chat_input("Schreibe 'Hallo' um zu starten..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 3. Stabiler Modell-Aufruf
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Wir schicken die Instruktion bei jeder Nachricht mit, 
        # das ist extrem stabil und vermeidet den v1beta-Fehler.
        full_context = f"Instruktion: {instruction}\n\nBisheriger Chat: {st.session_state.messages}\n\nNutzer: {prompt}"
        
        with st.spinner('Führungslabor verbindet...'):
            response = model.generate_content(full_context)
            
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Technisches Detail: {e}")
