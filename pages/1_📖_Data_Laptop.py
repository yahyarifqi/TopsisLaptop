import streamlit as st
from topsis import Topsis
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')

st.set_page_config(page_title="Data Laptop", page_icon="📖")
st.markdown("# Data Laptop")

st.write("""
    ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

    Di bawah adalah daftar laptop yang tersedia      
    """)

st.write(db.get_laptop_data())

if st.session_state["authentication_status"]:
    st.write('Masukkan CRUD di bawah ini')