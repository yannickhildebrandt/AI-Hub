import streamlit as st
import requests
import json

# URL deines n8n Webhook-Triggers (den bekommst du aus n8n)
N8N_WEBHOOK_URL = "https://n8n.srv1040466.hstgr.cloud/webhook-test/ee1cd20d-0adb-4df8-90a1-5e0032fb0719"

# --- Seiten-Konfiguration ---
st.set_page_config(page_title="Agentic Workflow Demo", layout="centered")

# --- Seiten-Inhalt ---
st.title("Willkommen beim Agentic Workflow! 🚀")
st.markdown("Werden Sie Teil einer Live-Demo und erhalten Sie im Anschluss personalisierte Informationen direkt von unserem Team.")

# WICHTIG: Das Bild wird nun von einer URL geladen, um den "FileNotFoundError" zu vermeiden.
# Laden Sie Ihr GIF z.B. bei https://imgur.com/upload hoch und ersetzen Sie den Link.
st.image("https://i.imgur.com/aQzaR2G.gif", caption="Dieser Prozess läuft gleich im Hintergrund für Sie ab.")

st.markdown("---")

# --- Eingabemaske ---
st.subheader("Erzählen Sie uns kurz von sich:")

with st.form("contact_form"):
    # NEU: Eingabefeld für den Vornamen
    first_name = st.text_input("Ihr Vorname*")
    
    # NEU: Schieberegler für die Kompetenzeinschätzung
    competence_level = st.slider(
        "Wie schätzen Sie Ihre aktuelle Kompetenz zu 'Agentic Workflows' ein?*",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = 'Noch nie gehört', 10 = 'Ich baue sie täglich'"
    )

    # NEU: Optionales Textfeld für den Use-Case
    use_case = st.text_area(
        "Welchen Anwendungsfall würden Sie gerne automatisieren? (Optional)",
        placeholder="z.B. Kundensupport-Anfragen vorsortieren, Rechnungen automatisch verarbeiten, Social-Media-Posts erstellen..."
    )

    # Bestehendes Feld für Kontaktinformation
    contact_info = st.text_input(
        "Ihre E-Mail-Adresse oder Telefonnummer (inkl. Ländervorwahl)*",
        placeholder="name@beispiel.de oder +4917612345678"
    )

    submitted = st.form_submit_button("Workflow starten & Informationen anfordern")

    if submitted:
        # Einfache Prüfung, ob die Pflichtfelder ausgefüllt sind
        if first_name and contact_info:
            try:
                # Daten als JSON-Payload an den n8n-Webhook senden
                payload = {
                    "firstName": first_name,
                    "competenceLevel": competence_level,
                    "useCase": use_case,
                    "emailOrPhone": contact_info
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
