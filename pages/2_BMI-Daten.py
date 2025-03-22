import streamlit as st
import pandas as pd

st.title("Werte")

st.write("Hier können Sie den Verlauf Ihrer Resultate sehen.")

# Überprüfen, ob 'data_df' in st.session_state existiert
if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    data_df = st.session_state['data_df']
    
    # Sortiere die Tabelle nach Zeitstempel
    data_df = data_df.sort_values('timestamp', ascending=False)
    
    # Tabelle anzeigen
    st.dataframe(data_df, use_container_width=True)
else:
    st.info("Keine Daten vorhanden. Geben Sie Ihre Werte im Rechner ein.")