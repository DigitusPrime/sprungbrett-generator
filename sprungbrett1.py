import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FM Sprungbrett", page_icon="🚀")
st.title("🚀 Dein Sprungbrett-Test")

# 1. Key laden und säubern (DAS IST DER HÄUFIGSTE FEHLER)
# Wir entfernen alle eckigen Klammern, Anführungszeichen und Leerzeichen!
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"].replace("[", "").replace("]", "").replace('"', "").replace("'", "").strip()
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Streamlit-Secrets!")
    st.stop()

# 2. Ein ganz simpler Prompt-Test
prompt = st.text_input("Schreibe etwas und drücke Enter:", "Hallo")

if st.button("KI fragen"):
    try:
        # Wir nutzen den absolut stabilsten Namen
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner('Prüfe Pro-Verbindung...'):
            # Einfachste Anfrage ohne Schnickschnack
            response = model.generate_content(f"Antworte nur mit: 'Verbindung steht, Zwi!'. Der User sagt: {prompt}")
            
        st.success(response.text)
        st.balloons()
        
    except Exception as e:
        st.error(f"Fehler-Details: {e}")
        st.info("Falls hier '404' steht, versuche in Streamlit 'Reboot App'.")
