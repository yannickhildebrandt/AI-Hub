import streamlit as st
import requests
import json

# URL deines n8n Webhook-Triggers
N8N_WEBHOOK_URL = "https://n8n.srv1040466.hstgr.cloud/webhook-test/ee1cd20d-0adb-4df8-90a1-5e0032fb0719"

# --- Seiten-Konfiguration ---
st.set_page_config(page_title="KI-Workflow Live-Demo", layout="centered")

# --- Seiten-Inhalt ---
st.title("Willkommen zur Live-Demo! 🚀")

st.markdown("""
Erleben Sie, wie wir KI-Workflows nutzen, um unseren Messealltag zu vereinfachen. 
Diese App startet unseren **ersten Workflow: den perfekten Gesprächseinstieg**.

Im Anschluss an unser Gespräch zeigen wir Ihnen gerne den **zweiten Workflow: das smarte Follow-up**, bei dem eine KI basierend auf einer kurzen Sprachnotiz eine komplette E-Mail mit den passenden Flyern für Sie vorbereitet.
""")

try:
    # Die Animation visualisiert, was im Hintergrund passiert, sobald Sie die Informationen absenden.
    st.image("workflow_animation.gif", caption="Dieser Prozess läuft gleich im Hintergrund für Sie ab.")
except Exception as e:
    st.warning("Info: Workflow-Animation konnte nicht geladen werden.")

st.markdown("---")

# --- Eingabemaske für Workflow 1 ---
st.subheader("Starten Sie den ersten Workflow: Der KI-Eisbrecher")
st.markdown("Geben Sie unten drei Stichworte zu Ihren Interessen ein. Unsere KI generiert daraus live einen personalisierten Gesprächsöffner für uns.")

# Datenschutz-Hinweis
st.info("✨ **Ihre Daten sind sicher:** Alle Eingaben werden DSGVO-konform und nur für den Zweck dieser Demo verarbeitet.")


with st.form("contact_form"):
    # Eingabefeld für den Vornamen
    first_name = st.text_input("Ihr Vorname*")
    
    # Schieberegler für die Kompetenzeinschätzung
    competence_level = st.slider(
        "Wie schätzen Sie Ihre aktuelle Kompetenz zu 'Agentic Workflows' ein?*",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = 'Noch nie gehört', 10 = 'Ich baue sie täglich'"
    )
    
    # Optionales Textfeld für den Use-Case
    use_case = st.text_area(
        "Welchen Anwendungsfall würden Sie gerne automatisieren? (Optional)",
        placeholder="z.B. Kundensupport-Anfragen vorsortieren, Rechnungen automatisch verarbeiten, Social-Media-Posts erstellen..."
    )
    
    # E-Mail-Feld (verpflichtend, ohne Telefonnummer)
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
                    "email": email  # Variable und Key angepasst
                }
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    data=json.dumps(payload),
                    headers={'Content-Type': 'application/json'}
                )
                
                # Prüfen, ob der Request erfolgreich war
                if response.status_code == 200:
                    st.success(f"Großartig, {first_name}! Der Workflow wurde gestartet. Sprechen Sie mich gerne direkt an – ich habe bereits alle Infos für einen perfekten Start.")
                    st.balloons()
                else:
                    st.error("Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.")
                    st.write("Fehler vom Server:", response.text)
            
            except requests.exceptions.RequestException as e:
                st.error(f"Verbindungsfehler zum Automatisierungs-Server: {e}")
        else:
            st.warning("Bitte füllen Sie alle Pflichtfelder (*) aus.")
