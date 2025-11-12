import streamlit as st
import requests
import json
import time # Importieren des time-Moduls

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
        st.caption("Basierend auf Ihren Eingaben im Formular unten erhält unser Team einen KI-generierten Vorschlag für den perfekten Gesprächseinstieg.")
    except Exception as e:
        st.warning("Info: Video für Workflow 1 konnte nicht geladen werden.")
with col2:
    st.markdown("##### Workflow 2: Das smarte Follow-up")
    try:
        # Video für den zweiten Workflow einbinden
        st.video("workflow2_animation.mp4")
        st.caption("Nach unserem Gespräch genügt eine Sprachnotiz: Die KI formuliert eine E-Mail, hängt die richtigen Flyer an und legt alles versandfertig in den Entwürfen ab.")
    except Exception as e:
        st.warning("Info: Video für Workflow 2 konnte nicht geladen werden.")

st.markdown("---")

# --- Beschreibung und Eingabemaske für Workflow 1 ---
st.subheader("Starten Sie den KI-Eisbrecher")
st.markdown("Geben Sie unten Ihre Daten ein, um live einen personalisierten Gesprächsöffner für uns zu generieren.")

st.info("✨ **Das Besondere:** Ihre Eingaben werden vollständig anonymisiert verarbeitet, auch wenn wir die Technologie führender KI-Anbieter nutzen. Ihre Privatsphäre ist geschützt.")

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

    st.markdown("""
    **Testen Sie es selbst!**  
    Für die Demo des Follow-ups benötigen wir eine E-Mail-Adresse. Falls Sie Ihre nicht angeben möchten, verwenden Sie einfach: **hildebrandt@eggers-partner.de**
    """)
    
    email = st.text_input(
        "Ihre E-Mail-Adresse*",
        placeholder="name@beispiel.de"
    )
    
    submitted = st.form_submit_button("Workflow starten & Gespräch beginnen")
    
    if submitted:
        if first_name and email:
            try:
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
                
                if response.status_code == 200:
                    # Bisherige Erfolgsmeldung bleibt
                    st.success(f"Großartig, {first_name}! Der Workflow wurde gestartet.")
                    st.balloons()

                    # --- NEUER TEIL: COUNTDOWN-TIMER ---
                    # 1. Einen leeren Platzhalter erstellen
                    timer_placeholder = st.empty()
                    
                    # 2. Schleife, die von 30 bis 0 herunterzählt
                    for seconds in range(45, -1, -1):
                        # 3. Nachricht formatieren und im Platzhalter anzeigen
                        message = f"Ein Mitarbeiter sollte sich in ca. **{seconds} Sekunden** bei Ihnen melden, um das Ergebnis und den zweiten Workflow zu zeigen."
                        timer_placeholder.info(message)
                        
                        # 4. Eine Sekunde warten
                        time.sleep(1)
                    
                    # 5. Finale Nachricht anzeigen, nachdem der Timer abgelaufen ist
                    timer_placeholder.success("Ein Mitarbeiter ist jetzt auf dem Weg zu Ihnen!")
                    # --- ENDE DES NEUEN TEILS ---

                else:
                    st.error("Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.")
                    st.write("Fehler vom Server:", response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Verbindungsfehler zum Automatisierungs-Server: {e}")
        else:
            st.warning("Bitte füllen Sie alle Pflichtfelder (*) aus.")
