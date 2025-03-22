import streamlit as st

st.title("Werte")

st.write("Hier können Sie den Verlauf ihrer Resultate sehen.")

data_df = st.session_state['data_df']
if data_df.empty:
    st.info('Keine Daten vorhanden. Geben Sie ihre Werte im Rechner ein.')
    st.stop()

# Sort dataframe by timestamp
data_df = data_df.sort_values('timestamp', ascending=False)

# Display table
st.dataframe(data_df)