import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# 1. Key laden und EXTREM gründlich reinigen
if "GOOGLE_API_KEY" in st.secrets:
    # Wir löschen wirklich alles, was kein Teil des Keys ist
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
    genai.configure(api_key=api_key)
else:
    st.error("Bitte API-Key in den Streamlit-Secrets hinterlegen!")
    st.stop()

# 2. Die Instruktion für das Führungslabor 2026
instruction = "Du bist der Sprungbrett-Generator. Prozess: 1. Hallo -> Energiefresser abfragen. 2. 1m/3m/5m abfragen. 3. Aktion & Reflexionsfrage ausgeben."

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nutzer-Eingabe
if prompt := st.chat_input("Schreibe 'Hallo'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # TRICK: Wir nutzen hier KEINE system_instruction im Aufruf, 
        # da dies oft den fehlerhaften v1beta-Pfad erzwingt!
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Wir bauen das Gedächtnis und die Anweisung händisch in den Prompt ein
        context = f"ANWEISUNG: {instruction}\n\nCHAT-HISTORIE: {st.session_state.messages[:-1]}\n\nAKTUELL: {prompt}"
        
        with st.spinner('Führungslabor verbindet...'):
            # Einfachste Anfrage-Form, die immer den stabilen Pfad nimmt
            response = model.generate_content(context)
            
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            st.error("KI hat keine Antwort gesendet. Bitte Seite neu laden.")

    except Exception as e:
        st.error(f"Technischer Stolperstein: {e}")
