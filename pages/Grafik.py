# Here starts the graph page
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime

st.title("Graph der Erythrozyten-Indizes")

# Überprüfen, ob Daten in der Session vorhanden sind
if 'data' not in st.session_state or not st.session_state['data']:
    st.write("Es sind keine Daten verfügbar, um die Grafik zu erstellen.")
else:
    # Erstelle einen DataFrame aus den gespeicherten Daten
    df = pd.DataFrame(st.session_state['data'])

    # Überprüfen, ob die erforderlichen Spalten vorhanden sind
    required_columns = ['Datum', 'MCV', 'MCH', 'MCHC', 'Resultat']
    if not all(col in df.columns for col in required_columns):
        st.write("Die erforderlichen Spalten sind in den Daten nicht vorhanden.")
    else:
        # Konvertiere die Datumsspalte in ein reines Datumsformat
        df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce').dt.date
        df = df.dropna(subset=['Datum'])

        # Erstelle den Scatterplot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Farben basierend auf dem Resultat
        color_map = {
            "Normochrom, Normozytär": "green",
            "Hypochrom, Mikrozytär": "red",
            "Hyperchrom, Makrozytär": "blue",
            "Andere": "orange"
        }
        df['Color'] = df['Resultat'].map(color_map).fillna("gray")

        # Scatterplot für MCV, MCH und MCHC
        scatter_mcv = ax.scatter(df['Datum'], df['MCV'], c=df['Color'], label='MCV', alpha=0.7)
        scatter_mch = ax.scatter(df['Datum'], df['MCH'], c=df['Color'], label='MCH', alpha=0.7)
        scatter_mchc = ax.scatter(df['Datum'], df['MCHC'], c=df['Color'], label='MCHC', alpha=0.7)

        # Achsentitel und Legende
        ax.set_xlabel('Datum')
        ax.set_ylabel('Werte')
        ax.legend()
        plt.xticks(rotation=45)

        # Plot in Streamlit anzeigen
        st.pyplot(fig)

        # Option zum Herunterladen der Grafik
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        file_name = f"scatter_plot_{datetime.now().strftime('%Y%m%d')}.png"
        st.download_button(
            label="Download Plot",
            data=buf,
            file_name=file_name,
            mime='image/png'
        )
