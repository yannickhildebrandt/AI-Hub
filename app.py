import streamlit as st
import requests
import json

# URL deines n8n Webhook-Triggers
N8N_WEBHOOK_URL = "https://n8n.srv1040466.hstgr.cloud/webhook/ee1cd20d-0adb-4df8-90a1-5e0032fb0719"

# --- Seiten-Konfiguration ---
st.set_page_config(page_title="KI-Workflow Live-Demo", layout="centered")

# --- Seiten-Inhalt ---
st.title("Willkommen zur Live-Demo! 🚀")

st.markdown("""
Erleben Sie, wie wir KI-Workflows nutzen, um unseren Messealltag zu vereinfachen.
Die Videos zeigen Ihnen zwei Beispiele: den perfekten Gesprächseinstieg und das automatisierte Follow-up.
""")

# --- Zwei Spalten für die Videos erstellen ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Workflow 1: Der KI-Eisbrecher")
    try:
        # Video für den ersten Workflow einbinden
        st.video("workflow1_animation.mp4")
        # NEU: Kurzbeschreibung unter dem Video
        st.caption("Basierend auf Ihren Eingaben im Formular unten erhält unser Team einen KI-generierten Vorschlag für den perfekten Gesprächseinstieg.")
    except Exception as e:
        st.warning("Info: Video für Workflow 1 konnte nicht geladen werden.")

with col2:
    st.markdown("##### Workflow 2: Das smarte Follow-up")
    try:
        # Video für den zweiten Workflow einbinden
        st.video("workflow2_animation.mp4")
        # NEU: Kurzbeschreibung unter dem Video
        st.caption("Nach unserem Gespräch genügt eine Sprachnotiz: Die KI formuliert eine E-Mail, hängt die richtigen Flyer an und legt alles versandfertig in den Entwürfen ab.")
    except Exception as e:
        st.warning("Info: Video für Workflow 2 konnte nicht geladen werden.")


st.markdown("---")


# --- Beschreibung und Eingabemaske für Workflow 1 ---
st.subheader("Starten Sie den KI-Eisbrecher")
st.markdown("Geben Sie unten Ihre Daten ein, um live einen personalisierten Gesprächsöffner für uns zu generieren.")

# Datenschutz-Hinweis
st.info("✨ **Ihre Daten sind sicher:** Alle Eingaben werden DSGVO-konform und nur für den Zweck dieser Demo verarbeitet.")

with st.form("contact_form"):
    
    first_name = st.text_input("Ihr Vorname*")
    
    competence_level = st.slider(
        "Wie schätzen Sie Ihre aktuelle Kompetenz zu 'Agentic Workflows' ein?*",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = 'Noch nie gehört', 10 = 'Ich baue sie täglich'"
    )
    
    use_case = st.text_area(
        "Welchen Anwendungsfall würden Sie gerne automatisieren? (Optional)",
        placeholder="z.B. Kundensupport-Anfragen vorsortieren, Rechnungen automatisch verarbeiten, Social-Media-Posts erstellen..."
    )
    
    # E-Mail-Feld als einziges, verpflichtendes Kontaktfeld
    email = st.text_input(
        "Ihre E-Mail-Adresse*",
        placeholder="name@beispiel.de"
    )
    
    submitted = st.form_submit_button("Workflow starten & Gespräch beginnen")
    
    if submitted:
        # Prüfung, ob die Pflichtfelder (Vorname und E-Mail) ausgefüllt sind
        if first_name and email:
            try:
                # Daten als JSON-Payload an den n8n-Webhook senden
                payload = {
                    "firstName": first_name,
                    "competenceLevel": competence_level,
                    "useCase": use_case,
                    "email": email
                }
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    data=json.dumps(payload),
                    headers={'Content-Type': 'application/json'}
                )
                
                # Prüfen, ob der Request erfolgreich war
                if response.status_code == 200:
                    st.success(f"Großartig, {first_name}! Der Workflow wurde gestartet. Sprechen Sie mich gerne direkt an – ich habe bereits alle Infos.")
                    st.balloons()
                else:
                    st.error("Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.")
                    st.write("Fehler vom Server:", response.text)
            
            except requests.exceptions.RequestException as e:
                st.error(f"Verbindungsfehler zum Automatisierungs-Server: {e}")
        else:
            st.warning("Bitte füllen Sie alle Pflichtfelder (*) aus.")
