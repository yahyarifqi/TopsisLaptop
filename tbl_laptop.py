import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement
import numpy as np

db = DbManagement('laptopsis.db')
# LAPTOP

data_laptop = db.read_laptop()

st.markdown("# DATA LAPTOP")

l_id = []
detailLink = []
laptopName = []
for data in data_laptop:
    data_l_id  = data[0]
    data_detailLink  = data[1]
    data_laptopName = data[2]

    l_id.append(data_l_id )
    detailLink .append(data_detailLink )
    laptopName.append(data_laptopName)

st.subheader("BACA DATA LAPTOP")
read_data_laptop = pd.DataFrame(data_laptop, columns=["l_id ","detailLink ","laptopName"])
st.write(read_data_laptop)
        
st.subheader("Tambah Data Laptop")
col1, col2, col3 = st.columns(3)
with col1:
    create_l_id  = st.text_input("ID")
with col2:
    create_detailLink  = st.text_input("Detail Link ")
with col3:
    create_laptopName = st.text_input("Laptop Name")
if st.button("Tambah", type='primary'):
    # Lakukan validasi input atau operasi lain jika diperlukan
    db.create_laptop(create_l_id , create_detailLink , create_laptopName)
    st.success("Data Discrete Criteria baru berhasil ditambah: l_id ={}, detaillink ={}, laptopname={}"
        .format(create_l_id , create_detailLink , create_laptopName))
    st.rerun()

st.subheader("Ubah Data Laptop")
list_of_laptop = [i[0] for i in data_laptop]
selected_laptop = st.selectbox("Data Laptop", list_of_laptop)
laptop_result = db.get_laptop(selected_laptop)

# Tampilkan data kategorisasi yang dipilih
if laptop_result:
    current_l_id  = laptop_result[0][0]
    current_detailLink  = laptop_result [0][1]
    current_laptopName = laptop_result[0][2]

    st.subheader("Form Ubah Data Laptop")
    col1, col2, col3 = st.columns(3)
    with col1:
        update_l_id  = st.text_input("Laptop", value=current_l_id )
    with col2:
        update_detailLink  = st.text_input("Criteria", value=current_detailLink )
    with col3:
        update_laptopName = st.text_input("Category", value=current_laptopName)

    if st.button("Ubah", type='primary'):
        # Lakukan validasi input atau operasi lain jika diperlukan
        db.update_laptop(update_l_id , update_detailLink , update_laptopName, 
                    current_l_id , current_detailLink , current_laptopName)
        st.success("Data Discrete Kategori berhasil diubah: ID={}, Detail Link ={}, Laptop Name={}".
            format(update_l_id , update_detailLink , update_laptopName))
        st.rerun()
else:
    st.warning("Data Laptop dengan ID {} tidak ditemukan.".format(update_l_id))

st.subheader("Hapus Data Laptop: {}".format(current_l_id))
if st.button("Hapus", type='primary'):
    db.delete_laptop(current_l_id, current_detailLink , current_laptopName)
    st.success("Data Laptop berhasil dihapus: '{}'".format(current_l_id))
    st.rerun()