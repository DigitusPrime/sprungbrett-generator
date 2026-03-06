import streamlit as st
import google.generativeai as genai
import os

# 1. Seite & Onboarding
st.set_page_config(page_title="FM Sprungbrett Pro", page_icon="🚀", layout="centered")

# --- NEU: Wertesystem aus .md Datei laden ---
def load_wertesystem():
    file_path = "Baumstark_Booklet_5._Auflage.md"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Allgemeine FM-Coaching Standards (Datei wertesystem.md nicht gefunden)."

WERTESYSTEM_TEXT = load_wertesystem()
# --------------------------------------------

st.title("🚀 Dein FM-Sprungbrett")
st.markdown("""
**Vom Energiefresser zur Aktion.**
Kennst du das? Kleine oder grosse Dinge im Führungsalltag rauben dir Energie, aber der erste Schritt zur Besserung fehlt. 
Das **Sprungbrett** ist dein Werkzeug, um vom Nachdenken ins Tun zu kommen.

Gemeinsam identifizieren wir heute einen **Energiefresser** und wählen dann die passende Sprungbretthöhe für deine Lösung. 
Je höher das Brett, desto mehr Mut ist gefragt – aber desto grösser ist auch die Befreiung.
""")

# 2. Seitenleiste: Nur Reset-Option
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

# 4. Chat-Historie & Anzeige
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- DYNAMISCHE ENTSCHEIDUNGSHILFE (Präzise Logik) ---
show_legend = False
if st.session_state.messages:
    last_ai_msg = ""
    for m in reversed(st.session_state.messages):
        if m["role"] == "assistant":
            last_ai_msg = m["content"].lower()
            break
    
    # Trigger: Erscheint nur bei der konkreten Nachfrage nach der Höhe
    trigger_words = ["1m", "3m", "5m", "1 meter", "3 meter", "5 meter", "sprungbretthöhe"]
    if any(word in last_ai_msg for word in trigger_words):
        show_legend = True

if show_legend:
    with st.expander("💡 Entscheidungshilfe: Was bedeuten die Sprungbretter?", expanded=True):
        st.markdown("""
| Höhe | Mut-Level | Beschreibung | Ziel |
| :--- | :--- | :--- | :--- |
| **1 Meter** | **Leicht** | Ein kleiner „Quick-Win“. Sofort umsetzbar (<15 Min). | Den Stein ins Rollen bringen. |
| **3 Meter** | **Respektabel** | Bewusste Verhaltensänderung oder klares Gespräch. | Spürbare Entlastung schaffen. |
| **5 Meter** | **Mutig** | Radikaler Stopp oder schwieriger Konflikt. | Echte Transformation & Klärung. |
""")

# 5. System-Instruktion
SYSTEM_INSTRUCTION = f"""
Du bist der Sprungbrett-Coach für das Führungslabor 2026. 
BASIS (Wegweiser aus deinem Wertesystem):
---
{WERTESYSTEM_TEXT}
---

DEINE AUFGABE:
1. Start: Wenn der User 'Hallo' sagt, begrüße ihn kurz und frage nach dem Energiefresser.
2. Klärung: Sobald der Energiefresser steht, frage explizit: 'Möchtest du vom 1m, 3m oder 5m Brett springen?'
3. Aktion: Gib eine AKTION und eine REFLEXIONSFRAGE aus, die exakt zur Höhe passen.
"""

# 6. Chat-Logik
if prompt := st.chat_input("Schreibe 'Hallo' um zu starten..."):
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
        st.error(f"Technisches Detail: {e}")
