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

data_categorization = db.read_categorization()

st.markdown("# DATA CATEGORIZATION")

ct_id = []
ct_specification= []
ct_criteria = []
ct_class = []
for data in data_categorization:
    data_ct_id = data[0]
    data_ct_specification = data[1]
    data_ct_criteria = data[2]
    data_ct_class = data[3]

    ct_id.append(data_ct_id)
    ct_specification.append(data_ct_specification)
    ct_criteria.append(data_ct_criteria)
    ct_class.append(data_ct_class)

st.subheader("BACA DATA CATEGORIZATION")
read_data_categorization = pd.DataFrame(data_categorization,columns=["id","specification","criteria", "class"])
st.write(read_data_categorization)
        
st.subheader("Tambah Data Kategorisasi")
col1, col2, col3 = st.columns(3)
with col1:
    create_id = st.text_input("id")
    create_specification = st.text_input("specification")
with col2:
    create_criteria = st.text_input("criteria")
    create_class = st.text_input("class")
if st.button("Tambah", type='primary'):
    # Lakukan validasi input atau operasi lain jika diperlukan
    db.create_categorization(create_id, create_specification, create_criteria, create_class)
    st.success("Data Kategorisasi baru berhasil ditambah: id{}, specification={}, criteria={}, class={}".format(
        create_id, create_specification, create_criteria, create_class))
    st.rerun()

st.subheader("Ubah Data Kategorisasi")
list_of_categrizations = [i[0] for i in data_categorization]
selected_categorization = st.selectbox("Data Categorization", list_of_categrizations)
categorization_result = db.get_categorization(selected_categorization)

# Tampilkan data kategorisasi yang dipilih
if categorization_result:

    # Form untuk mengubah data
    st.subheader("Form Ubah Data Kategorisasi")
    col1, col2, col3 = st.columns(3)
    with col1:
        update_id = st.text_input("Ubah ID", value=categorization_result[0][0])
        update_specification = st.text_input("Ubah Specification", value=categorization_result[0][1])
    with col2:
        update_criteria = st.text_input("Ubah Criteria", value=categorization_result[0][2])
    with col3:
        update_class = st.text_input("Ubah Class", value=categorization_result[0][3])
    
    if st.button("Ubah", type='primary'):
        # Lakukan validasi input atau operasi lain jika diperlukan
        db.update_categorization(update_id, update_specification, update_criteria, update_class, current_id, current_specification, current_criteria, current_class)
        st.success("Data Kategorization berhasil diubah: {}".format(update_id))
    st.rerun()
else:
    db.update_categorization(update_id, update_specification, update_criteria, update_class, current_id, current_specification, current_criteria, current_class)
    st.success("Data Kategorisasi berhasil di ubah: {}".format(update_id))


# try:
#     if st.session_state["authentication_status"]:
#         st.write('Masukkan CRUD di bawah ini')

#     data_categorization = db.read_categorization()

#     st.set_page_config(page_title='DATA CATEGORIZATION', page_icon= "📓")
#     st.markdown("# DATA CATEGORIZATION")

#     ct_id = []
#     ct_specification= []
#     ct_criteria = []
#     ct_class = []
#     for data in data_categorization:
#         data_ct_id = data[0]
#         data_ct_specification = data[2]
#         data_ct_criteria = data[3]
#         data_ct_class = data[4]

#         ct_id.append(data_ct_id)
#         ct_specification.append(data_ct_specification)
#         ct_criteria.append(data_ct_criteria)
#         ct_class.append(data_ct_class)
        
#         st.subheader("BACA DATA CATEGORIZATION")
#         read_data_categorization = pd.DataFrame(data_categorization,columns=["id","specification","criteria", "class"])
#         st.write(read_data_categorization)

# except:
#     pass
    