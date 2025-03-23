import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("Scatterplots der Erythrozyten-Indizes")

# Überprüfen, ob 'data_df' in st.session_state existiert
if 'data_df' not in st.session_state or st.session_state['data_df'].empty:
    st.info("Keine Daten vorhanden. Bitte geben Sie Ihre Werte im Rechner ein.")
    st.stop()

# Erstelle einen DataFrame aus den gespeicherten Daten
data_df = st.session_state['data_df']

# Sortiere die Tabelle nach Datum (neueste zuerst)
data_df = data_df.sort_values('Datum', ascending=False)

# Konvertiere die Datumsspalte in ein Datumsformat
data_df['Datum'] = pd.to_datetime(data_df['Datum'], errors='coerce')
data_df = data_df.dropna(subset=['Datum'])

# Scatterplot für MCV
fig, ax = plt.subplots()
ax.scatter(data_df['Datum'], data_df['MCV'], c='blue', label='MCV')
ax.set_title('MCV (Mittleres korpuskuläres Volumen) nach Datum')
ax.set_xlabel('Datum')
ax.set_ylabel('MCV (fL)')
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Scatterplot für MCH
fig, ax = plt.subplots()
ax.scatter(data_df['Datum'], data_df['MCH'], c='green', label='MCH')
ax.set_title('MCH (Mittleres korpuskuläres Hämoglobin) nach Datum')
ax.set_xlabel('Datum')
ax.set_ylabel('MCH (pg)')
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Scatterplot für MCHC
fig, ax = plt.subplots()
ax.scatter(data_df['Datum'], data_df['MCHC'], c='red', label='MCHC')
ax.set_title('MCHC (Mittlere korpuskuläre Hämoglobinkonzentration) nach Datum')
ax.set_xlabel('Datum')
ax.set_ylabel('MCHC (g/dL)')
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Option zum Herunterladen der Daten als CSV
csv = data_df.reset_index().to_csv(index=False).encode('utf-8')
st.download_button(
    label="Daten als CSV herunterladen",
    data=csv,
    file_name=f"erythrozyten_verlauf_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)