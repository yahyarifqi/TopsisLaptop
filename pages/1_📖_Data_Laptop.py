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

st.subheader("Form Ubah Data Discrete Kriteria")
col1, col2, col3 = st.columns(3)
with col1:
    title = st.text_input('Silahkan isi nama laptop?', '')
    st.write('Nama Laptop :', title)

    option = st.selectbox(
        'Silahkan pilih brand laptop?',
        ('HP', 'Dell', 'asus', 'lenovo', 'acer'))
    st.write('You selected:', option)

    option = st.selectbox(
        'Silahkan pilih brand laptop?',
        ('SSD', 'HDD', 'eMMc'))
    st.write('You selected:', option)

    title = st.text_input('Silahkan isi Durability', '')
    if title.isdigit():
        st.write('Nama Laptop:', title)
    else:
        st.warning('Input harus berupa angka.')

    option = st.selectbox(
        'Silahkan pilih Graphic Card',
        ('AMD Radeon', 'Intel UHD', 'NVDIA', 'Apple M2'))
    st.write('You selected:', option)

with col2:
    title = st.text_input('Masukan Harga terbaru', '')
    if title.isdigit():
        st.write('Harga Terbaru:', title)
    else:
        st.warning('Input harus berupa angka.')

    option = st.selectbox(
        'Silahkan pilih Processors',
        ('HP', 'Dell', 'asus', 'lenovo', 'acer'))
    st.write('You selected:', option)

    title = st.text_input('Silahkan isi Besar RAM', '')
    if title.isdigit():
        st.write('Besar RAM:', title)
    else:
        st.warning('Input harus berupa angka.')

    option = st.selectbox(
        'Silahkan pilih Processors',
        ('1920x1080', '1366x768'))
    st.write('You selected:', option)

    option = st.selectbox(
        'Silahkan pilih Size Screen',
        ('12.5', '14.0', '15.6', '11.6'))
    st.write('You selected:', option)
with col3:
    title = st.text_input('Masukan Harga Lama', '')
    if title.isdigit():
        st.write('Harga Lama:', title)
    else:
        st.warning('Input harus berupa angka.')

    option = st.selectbox(
        'Silahkan pilih Size Screen',
        ('512', '1.000', '500', '32'))
    st.write('You selected:', option)
    
    title = st.text_input('Masukan Berat Laptop', '')
    if title.isdigit():
        st.write('Berat Laptop:', title)
    else:
        st.warning('Input harus berupa angka.')

    title = st.text_input('Silahkan isi Link Laptop', '')
    st.write('Link Laptop :', title)


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
    