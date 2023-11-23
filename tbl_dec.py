import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
# DISCRETE CRITERIA

data_discrete_criteria = db.read_discrete_criteria()

st.markdown("# DATA DISCRETE CRITERIA")

laptop = []
criteria = []
category = []
for data in data_discrete_criteria:
    data_laptop = data[0]
    data_criteria = data[1]
    data_category = data[2]

    laptop.append(data_laptop)
    criteria.append(data_criteria)
    category.append(data_category)

st.subheader("BACA DATA DISCRETE CRITERIA")
read_data_discrete_criteria = pd.DataFrame(data_discrete_criteria, columns=["laptop","criteria","category"])
st.write(read_data_discrete_criteria)
        
st.subheader("Tambah Data Discrete Kriteria")
col1, col2, col3 = st.columns(3)
with col1:
    create_laptop = st.text_input("laptop")
with col2:
    create_criteria = st.text_input("criteria")
with col3:
    create_category = st.text_input("category")
if st.button("Tambah", type='primary'):
    # Lakukan validasi input atau operasi lain jika diperlukan
    db.create_discrete_criteria(create_laptop, create_criteria, create_category)
    st.success("Data Discrete Criteria baru berhasil ditambah: laptop={}, criteria={}, category={}"
        .format(create_laptop, create_criteria, create_category))
    st.rerun()

st.subheader("Ubah Data Discrete Kriteria")
list_of_discrete_criteria = [i[0] for i in data_discrete_criteria]
selected_discrete_criteria = st.selectbox("Data Discrete Kriteria", list_of_discrete_criteria)
discrete_criteria_result = db.get_discrete_criteria(selected_discrete_criteria)

# Tampilkan data kategorisasi yang dipilih
if discrete_criteria_result:
    current_laptop = discrete_criteria_result[0][0]
    current_criteria = discrete_criteria_result [0][1]
    current_category = discrete_criteria_result[0][2]

    st.subheader("Form Ubah Data Discrete Kriteria")
    col1, col2, col3 = st.columns(3)
    with col1:
        update_laptop = st.text_input("Laptop", value=current_laptop)
    with col2:
        update_criteria = st.text_input("Criteria", value=current_criteria)
    with col3:
        update_category = st.text_input("Category", value=current_category)

    if st.button("Ubah", type='primary'):
        # Lakukan validasi input atau operasi lain jika diperlukan
        db.update_discrete_criteria(update_laptop, update_criteria, update_category, 
                    current_laptop, current_criteria, current_category)
        st.success("Data Discrete Kategori berhasil diubah: Laptop={}, Criteria={}, Category={}".
            format(update_laptop, update_criteria, update_category))
        st.rerun()
else:
    st.warning("Data Discrete Kriteria dengan Laptop {} tidak ditemukan.".format(update_laptop))

st.subheader("Hapus Data Discrete Kriteria: {}".format(current_laptop))
if st.button("Hapus", type='primary'):
    db.delete_discrete_criteria(current_laptop, current_criteria, current_category)
    st.success("Data Discrete Kriteria berhasil dihapus: '{}'".format(current_laptop))
    st.rerun()