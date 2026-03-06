import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. Seite & Minimalistisches Onboarding
st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀")

st.title("🚀 Dein FM-Sprungbrett")
st.markdown("_Vom Energiefresser zur Aktion._")

# 2. Seitenleiste: Wissensbasis & Reset
st.sidebar.header("📁 Wissensbasis")
uploaded_file = st.sidebar.file_uploader("Wertesystem (PDF) hochladen", type="pdf")

values_context = ""
if uploaded_file:
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text: values_context += text
        st.sidebar.success("Wertesystem aktiv!")
    except Exception as e:
        st.sidebar.error(f"PDF-Fehler: {e}")

if st.sidebar.button("Neuen Dialog starten"):
    st.session_state.messages = []
    st.rerun()

# 3. API-Konfiguration (Gemini 2.5-flash)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
else:
    st.error("API-Key fehlt!")
    st.stop()

# 4. Chat-Historie & Anzeige
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- NEU: Dynamische Sprungbrett-Info ---
# Wir prüfen, ob die KI zuletzt nach der Höhe gefragt hat
show_legend = False
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant" and any(x in last_msg["content"].lower() for x in ["1m", "3m", "höhe", "sprungbretthöhe"]):
        show_legend = True

if show_legend:
    with st.expander("💡 Entscheidungshilfe: Welches Brett wählst du?", expanded=True):
        st.markdown("""
| Höhe | Mut-Level | Beschreibung |
| :--- | :--- | :--- |
| **1 Meter** | **Leicht** | Kleiner Quick-Win, sofort umsetzbar (<15 Min). |
| **3 Meter** | **Respektabel** | Bewusste Verhaltensänderung oder klares Gespräch. |
| **5 Meter** | **Mutig** | Radikaler Stopp oder schwieriger Konflikt. |
""")
# ---------------------------------------

# 5. Nutzer-Eingabe & KI-Logik
if prompt := st.chat_input("Schreibe 'Hallo' um zu starten..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Wir nutzen das Modell, das vorhin den "Volltreffer" gelandet hat
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # System-Instruktion (wird bei jedem Call mitgegeben)
        instruction = f"""
        Du bist der FM-Sprungbrett-Coach. 
        Wertesystem-Kontext: {values_context if values_context else "Standard FM-Werte."}
        
        Ablauf:
        1. Erst begrüßen & Energiefresser klären.
        2. Dann explizit nach 1m, 3m oder 5m fragen.
        3. Dann passende AKTION und REFLEXIONSFRAGE liefern.
        """
        
        history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        full_prompt = f"{instruction}\n\nHistorie:\n{history}\n\nKI:"
        
        with st.spinner('Sprungbrett wird justiert...'):
            response = model.generate_content(full_prompt)
            
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            # Falls die KI gerade nach der Höhe gefragt hat, triggert der nächste Loop den Expander
            st.rerun() 

    except Exception as e:
        st.error(f"Technisches Detail: {e}")
