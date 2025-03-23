import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Workspace2")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the file
data_manager.load_app_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    ) 
# ====== End Init Block ======

# here starts our app
st.title("Anämie-App")

st.markdown("""
#### App-Beschreibung
Version 0.1 der Anaemie-App für den Kurs Informatik 2. 
Diese App unterstuetzt Fachpersonen bei der Diagnose von Anaemien, indem sie praezise Laborwerte analysiert und interpretiert.  
Die App ist anhand der folgenden Formel programmiert:
- **MCV** = Referenzbereich (80-100 fl)
- **MCH** = Haemoglobin/RbC (27-34 pg)
- **MCHC** = Haemoglobin/Hkt (32-36 g/dl)
""")


st.write("Link zur App: https://workspace2.streamlit.app/Erythrozyten_Indices")


st.markdown("""
#### Autoren

- **Elena Mueller** (muellel3@students.zhaw.ch)
- **Kirisha Tharmaratnam** (tharmkir@students.zhaw.ch)
""")