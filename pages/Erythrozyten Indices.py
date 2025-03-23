# ====== Start Login Block ======
 
# ====== End Login Block ======

# ------------------------------------------------------------
# here starts our app

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("Erythrozyten Indices")

# Lade die CSV-Datei beim Start
if 'data_df' not in st.session_state:
    if os.path.exists("data_df.csv"):
        st.session_state['data_df'] = pd.read_csv("data_df.csv")
    else:
        st.session_state['data_df'] = pd.DataFrame(columns=['Datum', 'MCV', 'MCH', 'MCHC', 'Resultat'])

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

        st.session_state['data_df'] = pd.concat(
            [st.session_state['data_df'], pd.DataFrame([new_record])],
            ignore_index=True
        )

        # Speichere die aktualisierten Daten in die CSV-Datei
        try:
            st.session_state['data_df'].to_csv("data_df.csv", index=False)
            st.success("CSV-Datei erfolgreich aktualisiert.")
        except Exception as e:
            st.error(f"Fehler beim Aktualisieren der CSV-Datei: {e}")
    else:
        st.error("Bitte geben Sie gültige Werte ein.")