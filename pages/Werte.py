import streamlit as st
import pandas as pd

st.title("Erythrozyten-Werte")

st.write("Hier können Sie den Verlauf Ihrer Resultate sehen.")

# Überprüfen, ob 'data_df' in st.session_state existiert
if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    data_df = st.session_state['data_df']
    
    # Sortiere die Tabelle nach Datum (neueste zuerst)
    data_df = data_df.sort_values('Datum', ascending=False)
    
    # Tabelle anzeigen
    st.dataframe(data_df, use_container_width=True)

    # Option zum Herunterladen der Tabelle als CSV
    csv = data_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Daten als CSV herunterladen",
        data=csv,
        file_name="erythrozyten_daten.csv",
        mime="text/csv",
    )
else:
    st.info("Keine Daten vorhanden. Geben Sie Ihre Werte im Rechner ein.")