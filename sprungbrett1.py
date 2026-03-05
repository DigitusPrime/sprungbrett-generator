import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Dialog")

# 1. API-Konfiguration (Stabil für 2026)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Secrets!")
    st.stop()

# 2. Die Coaching-Instruktion (System-Kontext)
SYSTEM_PROMPT = """
Du bist der Sprungbrett-Coach für das Führungslabor. 
DEIN ZIEL: Hilf der Führungskraft, einen Energiefresser anzugehen.

ABLAUF (strikt einhalten):
1. Wenn der User 'Hallo' schreibt: Begrüsse ihn und frage: 'Welcher Energiefresser beschäftigt dich heute?'
2. Wenn der User den Energiefresser nennt: Frage nach der Sprungbretthöhe: 'Möchtest du vom 1m, 3m oder 5m Brett springen? (1m = kleiner Schritt, 5m = mutiger Sprung)'
3. Wenn die Höhe gewählt wurde: Gib eine konkrete AKTION und eine REFLEXIONSFRAGE aus.

TONFALL: Professionell, ermutigend, prägnant.
"""

# 3. Chat-Gedächtnis initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []

# Bisherigen Chat anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Nutzer-Eingabe verarbeiten
if prompt := st.chat_input("Schreibe 'Hallo' um zu starten..."):
    # Nutzer-Nachricht speichern und anzeigen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Wir nutzen das Modell, das wir vorhin erfolgreich getestet haben
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Wir bauen den gesamten Kontext zusammen
        full_context = f"{SYSTEM_PROMPT}\n\nBisheriger Chatverlauf: {st.session_state.messages}\n\nAktuelle Eingabe: {prompt}"
        
        with st.spinner('Sprungbrett wird vorbereitet...'):
            response = model.generate_content(full_context)
            
        # Antwort der KI anzeigen und speichern
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Ein technischer Energiefresser: {e}")

# Option zum Zurücksetzen
if st.sidebar.button("Neuen Dialog starten"):
    st.session_state.messages = []
    st.rerun()
