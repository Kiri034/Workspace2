import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("Scatterplots der Erythrozyten-Indizes")

# Überprüfen, ob 'data_df' in st.session_state existiert
if 'data_df' not in st.session_state or st.session_state['data_df'].empty:
    st.info("Es sind keine Daten verfügbar. Bitte geben Sie Ihre Werte im Rechner ein.")
    st.stop()

# Erstelle einen DataFrame aus den gespeicherten Daten
df = st.session_state['data_df']


# Überprüfen, ob die Spalte 'Datum' existiert
if 'Datum' in df.columns:
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
    df = df.dropna(subset=['Datum'])
else:
    st.error("Die Spalte 'Datum' fehlt in den Daten.")
    st.stop()

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