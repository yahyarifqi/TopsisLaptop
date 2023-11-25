import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
# NUMERIC CRITERIA

data_numeric_criteria = db.read_numeric_criteria()

st.markdown("# DATA NUMERIC CRITERIA")

laptop = []
criteria = []
value = []
for data in data_numeric_criteria:
    data_laptop = data[0]
    data_criteria = data[1]
    data_value = data[2]

    laptop.append(data_laptop)
    criteria.append(data_criteria)
    value.append(data_value)

st.subheader("BACA DATA NUMERIC CRITERIA")
read_data_numeric_criteria = pd.DataFrame(data_numeric_criteria, columns=["laptop","criteria","value"])
st.write(read_data_numeric_criteria)
        
st.subheader("Tambah Data Discrete Kriteria")
col1, col2, col3 = st.columns(3)
with col1:
    create_laptop = st.text_input("laptop")
with col2:
    create_criteria = st.text_input("criteria")
with col3:
    create_value = st.text_input("value")
if st.button("Tambah", type='primary'):
    # Lakukan validasi input atau operasi lain jika diperlukan
    db.create_numeric_criteria(create_laptop, create_criteria, create_value)
    st.success("Data Discrete Criteria baru berhasil ditambah: laptop={}, criteria={}, value={}"
        .format(create_laptop, create_criteria, create_value))
    st.rerun()

st.subheader("Ubah Data Discrete Kriteria")
list_of_numeric_criteria = [i[0] for i in data_numeric_criteria]
selected_numeric_criteria = st.selectbox("Data Discrete Kriteria", list_of_numeric_criteria)
numeric_criteria_result = db.get_numeric_criteria(selected_numeric_criteria)

# Tampilkan data kategorisasi yang dipilih
if numeric_criteria_result:
    current_laptop = numeric_criteria_result[0][0]
    current_criteria = numeric_criteria_result [0][1]
    current_value = numeric_criteria_result[0][2]

    st.subheader("Form Ubah Data Discrete Kriteria")
    col1, col2, col3 = st.columns(3)
    with col1:
        update_laptop = st.text_input("Laptop", value=current_laptop)
    with col2:
        update_criteria = st.text_input("Criteria", value=current_criteria)
    with col3:
        update_value = st.text_input("Value", value=current_value)

    if st.button("Ubah", type='primary'):
        # Lakukan validasi input atau operasi lain jika diperlukan
        db.update_numeric_criteria(update_laptop, update_criteria, update_value, 
                    current_laptop, current_criteria, current_value)
        st.success("Data Discrete Kategori berhasil diubah: Laptop={}, Criteria={}, Value={}".
            format(update_laptop, update_criteria, update_value))
        st.rerun()
else:
    st.warning("Data Discrete Kriteria dengan Laptop {} tidak ditemukan.".format(update_laptop))

st.subheader("Hapus Data Discrete Kriteria: {}".format(current_laptop))
if st.button("Hapus", type='primary'):
    db.delete_numeric_criteria(current_laptop, current_criteria, current_value)
    st.success("Data Discrete Kriteria berhasil dihapus: '{}'".format(current_laptop))
    st.rerun()