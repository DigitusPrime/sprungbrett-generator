import streamlit as st
import google.generativeai as genai

# Grundkonfiguration
st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")

st.title("🚀 Sprungbrett-Labor: Erholungsmodus")
st.info("Die App ist erfolgreich gestartet. Wir testen jetzt die Verbindung.")

# 1. Geheimnis-Check
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Fehler: Der 'GOOGLE_API_KEY' wurde in den Streamlit-Secrets nicht gefunden!")
    st.stop()

# 2. Verbindungstest auf Knopfdruck
if st.button("Verbindung zur KI jetzt testen"):
    try:
        # Key säubern (entfernt alle Klammern/Leerzeichen)
        api_key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'").strip("[").strip("]")
        
        # WICHTIG: Wir erzwingen die API-Version v1, um den 404-Fehler zu umgehen
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner('Sende Test-Anfrage an den Pro-Server...'):
            # Einfacher Test-Prompt
            response = model.generate_content("Antworte mit: 'System bereit!'")
            
        if response.text:
            st.success(f"✅ Erfolg! Die KI antwortet: {response.text}")
            st.balloons()
            st.session_state.ready = True
    except Exception as e:
        st.error(f"❌ Fehler bei der Verbindung: {str(e)}")
        st.info("Hinweis: Dein Billing ist aktiv (232 CHF), aber prüfe, ob der Key u0QA korrekt kopiert wurde.")

# 3. Kleiner Debug-Bereich (Nur für dich sichtbar)
with st.expander("Technisches Dashboard"):
    st.write("Eingetragener Key-Anfang:", st.secrets["GOOGLE_API_KEY"][:5] + "...")
    st.write("Modell: gemini-1.5-flash")
