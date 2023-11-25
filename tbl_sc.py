import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
# SUB CRITERIA

data_sub_criteria = db.read_sub_criteria()

st.markdown("# DATA Sub Kriteria")

cid = []
kelas = []
weight = []
for data in data_sub_criteria:
    data_cid  = data[0]
    data_kelas  = data[1]
    data_weight = data[2]

    cid.append(data_cid )
    kelas .append(data_kelas)
    weight.append(data_weight)

st.subheader("BACA DATA Sub Kriteria")
read_data_sub_criteria = pd.DataFrame(data_sub_criteria, columns=["id","kelas","weight"])
st.write(read_data_sub_criteria)
        
st.subheader("Tambah Sub Kriteria")
col1, col2, col3 = st.columns(3)
with col1:
    create_cid  = st.text_input("id")
with col2:
    create_kelas  = st.text_input("kelas")
with col3:
    create_weight = st.text_input("weight")
if st.button("Tambah", type='primary'):
    # Lakukan validasi input atau operasi lain jika diperlukan
    db.create_sub_criteria(create_cid , create_kelas , create_weight)
    st.success("Data Sub Criteria baru berhasil ditambah: id ={}, kelas ={}, weight ={}"
        .format(create_cid , create_kelas , create_weight))
    st.rerun()

st.subheader("Ubah Data Sub Kriteria")
list_of_sub_criteria = [i[0] for i in data_sub_criteria]
selected_sub_criteria = st.selectbox("Data Sub Criteria", list_of_sub_criteria)
sub_criteria_result = db.get_sub_criteria(selected_sub_criteria)

# Tampilkan data kategorisasi yang dipilih
if sub_criteria_result:
    current_cid  = sub_criteria_result[0][0]
    current_kelas  = sub_criteria_result [0][1]
    current_weight = sub_criteria_result[0][2]

    st.subheader("Form Ubah Data Sub Kriteria")
    col1, col2, col3 = st.columns(3)
    with col1:
        update_cid  = st.text_input("ID", value=current_cid )
    with col2:
        update_kelas  = st.text_input("Kelas", value=current_kelas )
    with col3:
        update_weight = st.text_input("Weight", value=current_weight)

    if st.button("Ubah", type='primary'):
        # Lakukan validasi input atau operasi lain jika diperlukan
        db.update_sub_criteria(update_cid , update_kelas , update_weight, 
                    current_cid , current_kelas , current_weight)
        st.success("Data Discrete Kategori berhasil diubah: ID={}, Kelas ={}, Weight ={}".
            format(update_cid , update_kelas , update_weight))
        st.rerun()
else:
    st.warning("Data Laptop dengan ID {} tidak ditemukan.".format(update_cid))

st.subheader("Hapus Data Sub Kriteria: {}".format(current_cid))
if st.button("Hapus", type='primary'):
    db.delete_sub_riteria(current_cid, current_kelas , current_weight)
    st.success("Data Sub Kriteria berhasil dihapus: '{}'".format(current_cid))
    st.rerun()