import streamlit as st
import pandas as pd

st.title("Werte")

st.write("Hier können Sie den Verlauf ihrer Resultate sehen.")

# Überprüfe, ob Daten vorhanden sind
if 'data' in st.session_state and st.session_state['data']:
    df = pd.DataFrame(st.session_state['data'])
    df['Datum'] = pd.to_datetime(df['Datum']).dt.strftime('%d.%m.%Y %H:%M:%S')
    st.dataframe(df, use_container_width=True)
else:
    st.write("Es sind noch keine Resultate verfügbar.")