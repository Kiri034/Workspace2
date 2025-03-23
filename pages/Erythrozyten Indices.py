# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======

# ------------------------------------------------------------
# here starts our app

import streamlit as st
import pandas as pd
from datetime import datetime
from webdav3.client import Client

st.title("Erythrozyten Indices")

# Lade Zugangsdaten aus secrets.toml
config = {
    'webdav_hostname': st.secrets["webdav"]["base_url"],
    'webdav_login': st.secrets["webdav"]["username"],
    'webdav_password': st.secrets["webdav"]["password"]
}

client = Client(config)

# Hochladen der Datei zu SwitchDrive
def upload_to_switchdrive(dataframe, remote_file):
    try:
        # Speichere die DataFrame-Daten in eine temporäre CSV-Datei
        temp_file = "temp_data.csv"
        dataframe.to_csv(temp_file, index=False)

        # Lade die Datei zu SwitchDrive hoch
        client.upload_sync(remote_path=remote_file, local_path=temp_file)
        st.success(f"Datei erfolgreich zu SwitchDrive hochgeladen: {remote_file}")
    except Exception as e:
        st.error(f"Fehler beim Hochladen zu SwitchDrive: {e}")

# Eingabefelder für Benutzer
hb = st.number_input("Hämoglobin (g/dL)", min_value=0.0, format="%.2f")
rbc = st.number_input("Erythrozytenzahl (10^12/L)", min_value=0.0, format="%.2f")
hct = st.number_input("Hämatokrit (%)", min_value=0.0, format="%.2f")

# Funktion zur Klassifikation
def classify_condition(mcv, mch, mchc):
    size_condition = "Normozytär"
    color_condition = "Normochrom"

    if mcv < 80:
        size_condition = "Mikrozytär"
    elif mcv > 100:
        size_condition = "Makrozytär"

    if mch < 27 or mchc < 33:
        color_condition = "Hypochrom"
    elif mch > 32 or mchc > 36:
        color_condition = "Hyperchrom"

    return f"{color_condition}, {size_condition}"

# Berechnung der Indizes
if st.button("Analysieren"):
    if hb > 0 and rbc > 0 and hct > 0:
        mcv = (hct / rbc) * 10
        mch = (hb / rbc) * 10
        mchc = (hb / hct) * 100

        result = classify_condition(mcv, mch, mchc)

        new_record = {
            'Datum': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'MCV': mcv,
            'MCH': mch,
            'MCHC': mchc,
            'Resultat': result
        }

        # Erstelle einen DataFrame mit den neuen Daten
        new_data_df = pd.DataFrame([new_record])

        # Lade die Datei direkt zu SwitchDrive hoch
        upload_to_switchdrive(new_data_df, "/remote_folder/data_df.csv")
    else:
        st.error("Bitte geben Sie gültige Werte ein.")