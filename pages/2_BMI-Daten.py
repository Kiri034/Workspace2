import streamlit as st
import pandas as pd
import os

st.title("Verlauf der Berechnungen")

# Funktion zum Laden der Verlaufsdaten
def load_history(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Datum", "Erythrozyten-Wert", "Ergebnis"])

# Funktion zum Speichern der Verlaufsdaten
def save_history(file_path, data):
    data.to_csv(file_path, index=False)

# Pfad zur CSV-Datei für den Verlauf
history_file = "erythrozyten_verlauf.csv"

# Verlaufsdaten laden
history_data = load_history(history_file)

# Verlauf anzeigen
if history_data.empty:
    st.info("Es sind noch keine Berechnungen im Verlauf gespeichert.")
else:
    st.subheader("Gespeicherte Berechnungen")
    st.dataframe(history_data, use_container_width=True)

    # Option zum Herunterladen der Verlaufsdaten
    csv = history_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Verlauf als CSV herunterladen",
        data=csv,
        file_name="erythrozyten_verlauf.csv",
        mime="text/csv",
    )

# Beispiel: Neue Daten hinzufügen (dieser Teil sollte in der Hauptberechnungsseite erfolgen)
if st.button("Beispieldaten hinzufügen"):
    new_entry = {
        "Datum": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Erythrozyten-Wert": 4.5,
        "Ergebnis": "Normal"
    }
    history_data = history_data.append(new_entry, ignore_index=True)
    save_history(history_file, history_data)
    st.success("Beispieldaten wurden hinzugefügt!")
    st.experimental_rerun()
