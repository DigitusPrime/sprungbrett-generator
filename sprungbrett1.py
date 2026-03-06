import streamlit as st
import google.generativeai as genai

# 1. Seite & Onboarding
st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀", layout="centered")

# --- HIER DEN TEXT DEINES WERTESYSTEMS EINTRAGEN ---
# Kopiere den Text deines PDFs einfach zwischen die Anführungszeichen.
WERTESYSTEM_TEXT = """
Hier den Text des betrieblichen Wertesystems einfügen...
Dieser Text dient der KI als dauerhafter Wegweiser.
"""
# --------------------------------------------------

st.title("🚀 Dein FM-Sprungbrett")
st.markdown("""
**Vom Energiefresser zur Aktion.**
Kennst du das? Kleine oder grosse Dinge im Führungsalltag rauben dir Energie, aber der erste Schritt zur Besserung fehlt. 
Das **Sprungbrett** ist dein Werkzeug, um vom Nachdenken ins Tun zu kommen.

Gemeinsam identifizieren wir heute einen **Energiefresser** und wählen dann die passende Sprungbretthöhe für deine Lösung. 
Je höher das Brett, desto mehr Mut ist gefragt – aber desto grösser ist auch die Befreiung.
""")

# 2. Seitenleiste: Nur Reset-Funktion
st.sidebar.header("📁 Optionen")
if st.sidebar.button("Neuen Dialog starten"):
    st.session_state.messages = []
    st.rerun()

# 3. API-Konfiguration
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
else:
    st.error("API-Key fehlt in den Secrets!")
    st.stop()

# 4. System-Instruktion (Nutzt jetzt den festen Text oben)
SYSTEM_INSTRUCTION = f"""
Du bist der Sprungbrett-Coach für das Führungslabor 2026. 
BASIS: Nutze dieses Wertesystem als Wegweiser:
---
{WERTESYSTEM_TEXT}
---

DEINE AUFGABE:
1. Start: Wenn der User 'Hallo' sagt, frage nach dem Energiefresser.
2. Klärung: Sobald der Energiefresser steht, frage explizit nach der Höhe (1m, 3m, 5m).
3. Aktion: Gib eine AKTION und eine REFLEXIONSFRAGE aus, die exakt zur Höhe passen.
"""

# 5. Chat-Historie anzeigen
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- DYNAMISCHER EXPANDER (Erscheint nur bei der Wahl) ---
show_mut_level = False
if st.session_state.messages:
    last_ai_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "")
    if any(keyword in last_ai_msg.lower() for keyword in ["1m", "3m", "5m", "höhe", "meter", "brett"]):
        show_mut_level = True

if show_mut_level:
    with st.expander("🔍 Entscheidungshilfe: Was bedeuten die Sprungbretter?", expanded=True):
        st.markdown("""
| Höhe | Mut-Level | Beschreibung | Ziel |
| :--- | :--- | :--- | :--- |
| **1 Meter** | **Leicht** | Ein kleiner „Quick-Win“. Wenig Risiko, sofort umsetzbar (<15 Min). | Den Stein ins Rollen bringen. |
| **3 Meter** | **Respektabel** | Eine bewusste Verhaltensänderung oder ein klares Gespräch. | Spürbare Entlastung schaffen. |
| **5 Meter** | **Mutig** | Ein radikaler Stopp oder ein schwieriger Konflikt. | Echte Transformation & Klärung. |
""")

# 6. Chat-Logik
if prompt := st.chat_input("Schreibe 'Hallo' um den Dialog zu beginnen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nHistorie:\n{history}\n\nKI:"
        
        with st.spinner('Berechne Absprungwinkel...'):
            response = model.generate_content(full_prompt)
            
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun() 
    except Exception as e:
        st.error(f"Technischer Stolperstein: {e}")
