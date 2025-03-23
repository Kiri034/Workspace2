import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Verlauf der Erythrozyten-Indizes")


if 'data' not in st.session_state:
    st.session_state['data'] = []

st.session_state['data'].append(new_record)
st.success("Daten erfolgreich gespeichert!")

# Überprüfen, ob Daten in der Session vorhanden sind
if 'data' not in st.session_state or not st.session_state['data']:
    st.info("Es sind keine Daten verfügbar. Bitte geben Sie Ihre Werte im Rechner ein.")
    st.stop()

# Erstelle einen DataFrame aus den gespeicherten Daten
df = pd.DataFrame(st.session_state['data'])

# Überprüfen, ob die erforderlichen Spalten vorhanden sind
required_columns = ['Datum', 'MCV', 'MCH', 'MCHC']
if not all(col in df.columns for col in required_columns):
    st.error("Die erforderlichen Spalten sind in den Daten nicht vorhanden.")
    st.stop()

# Konvertiere die Datumsspalte in ein Datumsformat und setze sie als Index
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
df = df.dropna(subset=['Datum'])
df = df.set_index('Datum')

# Diagramm für MCV über die Zeit
st.line_chart(data=df['MCV'], use_container_width=True)
st.caption('MCV (Mittleres korpuskuläres Volumen) über die Zeit (fL)')

# Diagramm für MCH über die Zeit
st.line_chart(data=df['MCH'], use_container_width=True)
st.caption('MCH (Mittleres korpuskuläres Hämoglobin) über die Zeit (pg)')

# Diagramm für MCHC über die Zeit
st.line_chart(data=df['MCHC'], use_container_width=True)
st.caption('MCHC (Mittlere korpuskuläre Hämoglobinkonzentration) über die Zeit (g/dL)')

# Option zum Herunterladen der Daten als CSV
csv = df.reset_index().to_csv(index=False).encode('utf-8')
st.download_button(
    label="Daten als CSV herunterladen",
    data=csv,
    file_name=f"erythrozyten_verlauf_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)