import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("Scatterplots der Erythrozyten-Indizes")

# Überprüfen, ob 'data' in st.session_state existiert
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

# Konvertiere die Datumsspalte in ein Datumsformat
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
df = df.dropna(subset=['Datum'])

# Scatterplot für MCV
fig, ax = plt.subplots()
ax.scatter(df['Datum'], df['MCV'], c='blue', label='MCV')
ax.set_title('MCV (Mittleres korpuskuläres Volumen) nach Datum')
ax.set_xlabel('Datum')
ax.set_ylabel('MCV (fL)')
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)

# Scatterplot für MCH
fig, ax = plt.subplots()
ax.scatter(df['Datum'], df['MCH'], c='green', label='MCH')
ax.set_title('MCH (Mittleres korpuskuläres Hämoglobin) nach Datum')
ax.set_xlabel('Datum')
ax.set_ylabel('MCH (pg)')
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)

# Scatterplot für MCHC
fig, ax = plt.subplots()
ax.scatter(df['Datum'], df['MCHC'], c='red', label='MCHC')
ax.set_title('MCHC (Mittlere korpuskuläre Hämoglobinkonzentration) nach Datum')
ax.set_xlabel('Datum')
ax.set_ylabel('MCHC (g/dL)')
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)

# Option zum Herunterladen der Daten als CSV
csv = df.reset_index().to_csv(index=False).encode('utf-8')
st.download_button(
    label="Daten als CSV herunterladen",
    data=csv,
    file_name=f"erythrozyten_verlauf_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)