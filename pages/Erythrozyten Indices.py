import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


st.title("Erythrozyten Indices")

# Initialisiere 'data_df' in st.session_state, falls es nicht existiert
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame(columns=[
        "Datum", "Haemoglobin (g/dL)", "Erythrozytenzahl (10^12/L)", 
        "Haematokrit (%)", "MCV (fL)", "MCH (pg)", "MCHC (g/dL)", "Resultat"
    ])

# Input fields for user to enter values
hb = st.number_input("Haemoglobin (g/dL)", min_value=0.0, format="%.2f")
rbc = st.number_input("Erythrozytenzahl (10^12/L)", min_value=0.0, format="%.2f")
hct = st.number_input("Haematokrit (%)", min_value=0.0, format="%.2f")

def classify_condition(mcv, mch, mchc):
    size_condition = "Normozytaer"
    color_condition = "Normochrom"
    
    if mcv < 80:
        size_condition = "Mikrozytaer"
    elif mcv > 100:
        size_condition = "Makrozytaer"
    
    if mch < 27 or mchc < 33:
        color_condition = "Hypochrom"
    elif mch > 32 or mchc > 36:
        color_condition = "Hyperchrom"
    
    return f"{color_condition}, {size_condition}"

# Calculate Erythrozyten Indices
if st.button("Analysieren", key="analyze_button", help="Klicken Sie hier, um die Analyse durchzufuehren", use_container_width=True):
    if hb > 0 and rbc > 0 and hct > 0:
        mcv = (hct / rbc) * 10
        mch = (hb / rbc) * 10
        mchc = (hb / hct) * 100

        st.write(f"Mittleres korpuskulaeres Volumen (MCV): {mcv:.2f} fL")
        st.write(f"Mittleres korpuskulaeres Haemoglobin (MCH): {mch:.2f} pg")
        st.write(f"Mittlere korpuskulaere Haemoglobinkonzentration (MCHC): {mchc:.2f} g/dL")

        result = classify_condition(mcv, mch, mchc)
        
        if result == "Normochrom, Normozytaer":
            st.write(f"Resultat: {result}")
        else:
            st.markdown(f"<span style='color:red'>Resultat: {result}</span>", unsafe_allow_html=True)

        # update the data.csv file
        from utils.data_manager import DataManager
        # Create a new record with the calculated values
        new_record = {
            "Datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Haemoglobin (g/dL)": hb,
            "Erythrozytenzahl (10^12/L)": rbc,
            "Haematokrit (%)": hct,
            "MCV (fL)": mcv,
            "MCH (pg)": mch,
            "MCHC (g/dL)": mchc,
            "Resultat": result
        }
        DataManager().append_record(session_state_key='data_df', record_dict=new_record)

        st.success("Daten erfolgreich gespeichert.")
    else:
        st.error("Bitte geben Sie gültige Werte für Hämoglobin, Erythrozytenzahl und Haematokrit ein.")


# CSS to style the button in red and make it smaller
st.markdown("""
    <style>
    .stButton button {
        background-color: red;
        color: white;
        font-size: 10px;  /* Reduced font size */
        padding: 4px 8px;  /* Reduced padding */
    }
    </style>
    """, unsafe_allow_html=True)
