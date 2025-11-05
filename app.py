import streamlit as st
import requests
import json

# URL deines n8n Webhook-Triggers (den bekommst du aus n8n)
N8N_WEBHOOK_URL = "DEINE_N8N_WEBHOOK_URL_HIER_EINFÜGEN"

# --- Seiten-Konfiguration ---
st.set_page_config(page_title="Agentic Workflow Demo", layout="centered")

# --- Seiten-Inhalt ---

st.title("Willkommen beim Agentic Workflow! 🚀")
st.markdown("Sie sind jetzt Teil einer live-demonstrierten Automatisierung. Geben Sie Ihre Kontaktdaten ein, um eine personalisierte Nachricht zu erhalten.")

# Hier kannst du ein GIF oder Bild deines Workflows einfügen
# Lade das GIF in dasselbe Verzeichnis wie dein Skript hoch.
st.image("workflow_animation.gif", caption="So läuft der Prozess im Hintergrund ab.")

st.markdown("---")

# --- Eingabemaske ---
with st.form("contact_form"):
    contact_info = st.text_input(
        "Ihre E-Mail-Adresse oder Telefonnummer (inkl. Ländervorwahl, z.B. +49176...)",
        placeholder="name@beispiel.de oder +4917612345678"
    )
    submitted = st.form_submit_button("Workflow starten!")

    if submitted:
        if contact_info:
            try:
                # Daten als JSON an den n8n-Webhook senden
                payload = {"emailOrPhone": contact_info}
                response = requests.post(N8N_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

                # Prüfen, ob der Request erfolgreich war
                if response.status_code == 200:
                    st.success(f"Großartig! Der Workflow wurde für '{contact_info}' gestartet. Sie erhalten in Kürze eine Nachricht.")
                    st.balloons()
                else:
                    st.error("Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.")
                    st.write("Status Code:", response.status_code)

            except requests.exceptions.RequestException as e:
                st.error(f"Verbindungsfehler zum Automatisierungs-Server: {e}")
        else:
            st.warning("Bitte geben Sie eine E-Mail-Adresse oder Telefonnummer ein.")
