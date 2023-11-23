import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')

st.set_page_config(page_title="Data Laptop", page_icon="📖")
st.markdown("# Data Laptop")

st.write("""
    ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

    Di bawah adalah daftar laptop yang tersedia      
    """)

st.write(db.get_laptop_data())

try:
    if st.session_state["authentication_status"]:
        st.write('Masukkan CRUD di bawah ini')
except:
    pass
    data_categorization = db.read_categorization()

    st.set_page_config(page_title='DATA CATEGORIZATION', page_icon= "📓")
    st.markdown("# DATA CATEGORIZATION")

    ct_id = []
    ct_specification= []
    ct_criteria = []
    ct_class = []
    for data in data_categorization:
        data_ct_id = data[0]
        data_ct_specification = data[2]
        data_ct_criteria = data[3]
        data_ct_class = data[4]

        ct_id.append(data_ct_id)
        ct_specification.append(data_ct_specification)
        ct_criteria.append(data_ct_criteria)
        ct_class.append(data_ct_class)
        
        st.subheader("BACA DATA CATEGORIZATION")
        read_data_categorization = pd.DataFrame(data_categorization,columns=["id","specification","criteria", "class"])
        st.write(read_data_categorization)