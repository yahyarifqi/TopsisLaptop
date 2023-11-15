import streamlit as st
from topsis import Topsis
from dbmanagement import DbManagement
db = DbManagement('laptopsis.db')

def init():
    #Import tabel-tabel yang diperlukan
    db = DbManagement('laptopsis.db')
    data =  db.get_laptop_data(for_topsis=True)

    criteria = db.get_criteria()
    criteria = criteria.set_index('criteria')

    subcrit = db.get_sub_criteria()

    return data, criteria, subcrit

st.set_page_config(page_title="Data Laptop", page_icon="📖")
st.markdown("# Data Laptop")
st.sidebar.header("Data Laptop")

st.write("""
    ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

    Di bawah adalah daftar laptop yang tersedia      
    """)

data, criteria, subcrit = init()
st.write(db.get_laptop_data())