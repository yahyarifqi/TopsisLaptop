import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
# DATA CRITERIA

data_criteria = db.read_criteria()

st.markdown("# DATA CRITERIA")

cr_id = []
cr_criteria = []
cr_text = []
cr_weight = []
cr_impact = []
cr_type = []
cr_weighted = []
for data in data_criteria:
    data_cr_id = data[0]
    data_cr_criteria = data[1]
    data_cr_text = data[2]
    data_cr_weight = data[3]
    data_cr_impact = data[4]
    data_cr_type = data[5]
    data_cr_weighted = data[6]

    cr_id.append(data_cr_id)
    cr_criteria.append(data_cr_criteria)
    cr_text.append(data_cr_text)
    cr_weight.append(data_cr_weight)
    cr_impact.append(data_cr_impact)
    cr_type.append(data_cr_type)
    cr_weighted.append(data_cr_weight)

st.subheader("BACA DATA CRITERIA")
read_data_criteria = pd.DataFrame(data_criteria, columns=["id","criteria","text", "weight", "impact", "type", "weighted"])
st.write(read_data_criteria)
        
st.subheader("Tambah Data Kriteria")
col1, col2, col3 = st.columns(3)
with col1:
    create_id = st.text_input("id")
    create_criteria = st.text_input("criteria")
    create_text = st.text_input("text")
with col2:
    create_weight = st.text_input("weight")
    create_impact = st.text_input("impact")
with col3:
    create_type = st.text_input("type")
    create_weighted = st.text_input("weighted")
if st.button("Tambah", type='primary'):
    # Lakukan validasi input atau operasi lain jika diperlukan
    db.create_criteria(create_id, create_criteria, create_text, create_weight, create_impact, create_type, create_weighted)
    st.success("Data Kategorisasi baru berhasil ditambah: id{}, criteria={}, text={}, weight={}, impact={}, type={}, weighted={}"
        .format(create_id, create_criteria, create_text, create_weight, create_impact, create_type, create_weighted))
    st.rerun()

st.subheader("Ubah Data Kriteria")
list_of_criteria = [i[0] for i in data_criteria]
selected_criteria = st.selectbox("Data Criteria", list_of_criteria)
criteria_result = db.get_criteria(selected_criteria)

# Tampilkan data kategorisasi yang dipilih
if criteria_result:
    current_id = criteria_result[0][0]
    current_criteria = criteria_result [0][1]
    current_text = criteria_result[0][2]
    current_weight = criteria_result[0][3]
    current_impact = criteria_result [0][4]
    current_type = criteria_result[0][5]
    current_weighted = criteria_result[0][6]


    st.subheader("Form Ubah Data Kategorisasi")
    col1, col2, col3 = st.columns(3)
    with col1:
        update_id = st.text_input("ID", value=current_id)
        update_criteria = st.text_input("Criteria", value=current_criteria)
        update_text = st.text_input("Text", value=current_text)
    with col2:
        update_weight = st.text_input("Weight", value=current_weight)
        update_impact = st.text_input("Impact", value=current_impact)
    with col3:
        update_type = st.text_input("Type", value=current_type)
        update_weighted = st.text_input("Weighted", value=current_weighted)

    if st.button("Ubah", type='primary'):
        # Lakukan validasi input atau operasi lain jika diperlukan
        db.update_criteria(update_id, update_criteria, update_text, update_weight, update_impact, update_type, update_weighted, 
        current_id, current_criteria, current_text, current_weight, current_impact, current_type, current_weighted)
        st.success("Data Kriteria berhasil diubah: ID={}, Criteria={}, Text={}, weight={}, impact={}, type={}, weighted={}".
            format(update_id, update_criteria, update_text, update_weight, update_impact, update_type, update_weighted))
        st.rerun()
else:
    st.warning("Data Kriteria dengan ID {} tidak ditemukan.".format(update_id))

st.subheader("Hapus Data Kriteria: {}".format(current_id))
if st.button("Hapus", type='primary'):
    db.delete_criteria(current_id, current_criteria, current_text, current_weight, current_impact, current_type, current_weighted)
    st.success("Data Kriteria berhasil dihapus: '{}'".format(current_id))
    st.rerun()