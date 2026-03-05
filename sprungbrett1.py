import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Check")

# 1. Key extrem sicher laden
if "GOOGLE_API_KEY" in st.secrets:
    # Wir löschen ALLES, was kein Buchstabe oder Zahl des Keys ist
    api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Streamlit-Secrets!")
    st.stop()

# 2. Diagnose-Funktion: Was darf der Key?
if st.sidebar.button("System-Diagnose"):
    try:
        models = [m.name for m in genai.list_models()]
        st.sidebar.write("Verfügbare Modelle:", models)
    except Exception as e:
        st.sidebar.error(f"Diagnose fehlgeschlagen: {e}")

# 3. Das eigentliche Tool
instruction = "Du bist der Sprungbrett-Generator. Start: Hallo. Dann Energiefresser. Dann 1m/3m/5m. Dann Aktion & Reflexion."

if prompt := st.chat_input("Schreibe 'Hallo' für den Test..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # TRICK: Wir nutzen hier KEINE System_instruction beim Erstellen,
        # da dies oft den fehlerhaften v1beta-Pfad erzwingt!
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Wir schicken die Anweisung direkt im Text mit
        full_prompt = f"SYSTEM: {instruction}\n\nUSER: {prompt}"
        
        with st.spinner('Verbindung zum Pro-Server wird gesichert...'):
            response = model.generate_content(full_prompt)
            
        if response and response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
        else:
            st.error("Die KI hat keine Daten geliefert. Prüfe das Billing.")

    except Exception as e:
        st.error(f"Technisches Detail: {e}")
        st.info("Falls hier immer noch 'v1beta' steht, müssen wir die 'Generative Language API' in der Cloud Console prüfen.")
