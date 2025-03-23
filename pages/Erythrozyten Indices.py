# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# ------------------------------------------------------------
# here starts our app
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager

st.title("Erythrozyten Indices")

# Initialisiere session_state['data_df'], falls es nicht existiert
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame(columns=['Datum', 'MCV', 'MCH', 'MCHC', 'Resultat'])

# Eingabefelder für Benutzer
hb = st.number_input("Hämoglobin (g/dL)", min_value=0.0, format="%.2f")
rbc = st.number_input("Erythrozytenzahl (10^12/L)", min_value=0.0, format="%.2f")
hct = st.number_input("Hämatokrit (%)", min_value=0.0, format="%.2f")

# Funktion zur Klassifikation
def classify_condition(mcv, mch, mchc):
    size_condition = "Normozytär"
    color_condition = "Normochrom"

    if mcv < 80:
        size_condition = "Mikrozytär"
    elif mcv > 100:
        size_condition = "Makrozytär"

    if mch < 27 or mchc < 33:
        color_condition = "Hypochrom"
    elif mch > 32 or mchc > 36:
        color_condition = "Hyperchrom"

    return f"{color_condition}, {size_condition}"

# Berechnung der Indizes
if st.button("Analysieren", key="analyze_button", help="Klicken Sie hier, um die Analyse durchzuführen", use_container_width=True):
    if hb > 0 and rbc > 0 and hct > 0:
        mcv = (hct / rbc) * 10
        mch = (hb / rbc) * 10
        mchc = (hb / hct) * 100

        st.write(f"Mittleres korpuskuläres Volumen (MCV): {mcv:.2f} fL")
        st.write(f"Mittleres korpuskuläres Hämoglobin (MCH): {mch:.2f} pg")
        st.write(f"Mittlere korpuskuläre Hämoglobinkonzentration (MCHC): {mchc:.2f} g/dL")

        result = classify_condition(mcv, mch, mchc)

        if result == "Normochrom, Normozytär":
            st.write(f"Resultat: {result}")
        else:
            st.markdown(f"<span style='color:red'>Resultat: {result}</span>", unsafe_allow_html=True)

        # Speichere die aktuellen Werte in session_state
        new_record = {
            'Datum': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'MCV': mcv,
            'MCH': mch,
            'MCHC': mchc,
            'Resultat': result
        }
        # Entferne leere Werte aus dem Dict
        new_record = {k: v for k ,v in new_record.items() if k in st.session_state['data_df'].columns}

        # Füge den neuen Datensatz zu session_state['data_df'] hinzu
        st.session_state['data_df'] = pd.concat(
            [st.session_state['data_df'], pd.DataFrame([new_record])],
            ignore_index=True
        )

        # Speichere die Daten mit DataManager
        try:
            data_manager = DataManager()
            data_manager.append_record(session_state_key='data_df', record_dict=new_record)
            st.success("Daten erfolgreich gespeichert.")
        except ValueError as e:
            st.error(f"Fehler: {e}")
        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    else:
        st.error("Bitte geben Sie gültige Werte für Hämoglobin, Erythrozytenzahl und Hämatokrit ein.")