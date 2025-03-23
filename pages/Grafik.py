import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Verlauf der Erythrozyten-Indizes")

# Überprüfen, ob 'data_df' in st.session_state existiert
if 'data_df' not in st.session_state or st.session_state['data_df'].empty:
    st.info("Keine Daten vorhanden. Bitte geben Sie Ihre Werte im Rechner ein.")
    st.stop()

# Erstelle einen DataFrame aus den gespeicherten Daten
data_df = st.session_state['data_df']

# Sortiere die Tabelle nach Datum (neueste zuerst)
data_df = data_df.sort_values('Datum', ascending=False)

# Konvertiere die Datumsspalte in ein Datumsformat und setze sie als Index
data_df['Datum'] = pd.to_datetime(data_df['Datum'], errors='coerce')
data_df = data_df.dropna(subset=['Datum'])
data_df = data_df.set_index('Datum')

# Diagramm für MCV über die Zeit
st.line_chart(data=data_df['MCV'], use_container_width=True)
st.caption('MCV (Mittleres korpuskuläres Volumen) über die Zeit (fL)')

# Diagramm für MCH über die Zeit
st.line_chart(data=data_df['MCH'], use_container_width=True)
st.caption('MCH (Mittleres korpuskuläres Hämoglobin) über die Zeit (pg)')

# Diagramm für MCHC über die Zeit
st.line_chart(data=data_df['MCHC'], use_container_width=True)
st.caption('MCHC (Mittlere korpuskuläre Hämoglobinkonzentration) über die Zeit (g/dL)')

# Option zum Herunterladen der Daten als CSV
csv = data_df.reset_index().to_csv(index=False).encode('utf-8')
st.download_button(
    label="Daten als CSV herunterladen",
    data=csv,
    file_name=f"erythrozyten_verlauf_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)