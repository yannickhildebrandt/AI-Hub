import streamlit as st
import requests
import json

# URL deines n8n Webhook-Triggers
N8N_WEBHOOK_URL = "https://n8n.srv1040466.hstgr.cloud/webhook/ee1cd20d-0adb-4df8-90a1-5e0032fb0719"

# --- Seiten-Konfiguration ---
st.set_page_config(page_title="KI-Workflow Live-Demo", layout="centered")

# --- Seiten-Inhalt ---
st.title("Willkommen zur Live-Demo! 🚀")

# Angepasster Einleitungstext gemäß Variante 1
st.markdown("""
Erleben Sie, wie wir KI-Workflows nutzen, um unseren Messealltag zu vereinfachen.
Diese App zeigt Ihnen zwei Beispiele: den perfekten Gesprächseinstieg und das automatisierte Follow-up.
""")

try:
    # Die Animation visualisiert, was im Hintergrund passiert, sobald Sie die Informationen absenden.
    st.image("Video-Workflow2.gif", caption="Die Animationen visualisieren, was im Hintergrund passiert, sobald Sie die Informationen absenden.")
except Exception as e:
    st.warning("Info: Workflow-Animation konnte nicht geladen werden.")

st.markdown("---")


# --- Beschreibung und Eingabemaske für Workflow 1 ---
st.subheader("Workflow 1: Der KI-Eisbrecher")
st.markdown("Geben Sie unten drei Stichworte zu Ihren Interessen ein. Unsere KI generiert daraus live einen personalisierten Gesprächsöffner für uns.")

# Datenschutz-Hinweis, der den Aspekt der Anonymisierung verantwortungsvoll aufgreift
st.info("✨ **Das Besondere:** Ihre Eingaben werden vollständig DSGVO-konform verarbeitet. Obwohl wir die Technologie führender KI-Anbieter nutzen, ist Ihre Privatsphäre geschützt.")

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
                    "email": email  # Variable und Key angepasst an "email"
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

st.markdown("---")

# --- Beschreibung für Workflow 2 ---
st.subheader("Workflow 2: Das smarte Follow-up")
st.markdown("""
Nach unserem Gespräch reicht eine kurze Sprachnotiz als Zusammenfassung. Die KI erledigt den Rest:
*   Formuliert eine professionelle Follow-up-E-Mail.
*   Lädt automatisch zwei relevante Flyer herunter und fügt sie als Anhang hinzu.
*   Legt die fertige E-Mail im richtigen Entwurfsordner ab – bereit zum Senden.

**Sprechen Sie uns an, wir zeigen es Ihnen gerne live!**
""")
