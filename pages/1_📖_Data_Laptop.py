import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement
from streamlit.components.v1 import html


db = DbManagement('laptopsis.db')

st.set_page_config(page_title="Data Laptop", page_icon="📖")
st.markdown("# Data Laptop")

st.write("""
    ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

    Di bawah adalah daftar laptop yang tersedia      
    """)

st.write(db.get_laptop_data())

tab1, tab2= st.tabs(["CREAT", "UPDATE"])

with tab1:

    def tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, besar_ram, ketahanan_baterai,
                    harga_terbaru, harga_lama, link_laptop):
        # Di sini, Anda dapat menambahkan logika untuk menyimpan data ke database atau melakukan operasi lainnya
        st.success(f"Data berhasil ditambahkan:\n"
                f"Nama Laptop: {nama_laptop}\n"
                f"Brand Laptop: {brand_laptop}\n"
                f"Tipe Penyimpanan: {tipe_penyimpanan}\n"
                f"Jumlah Penyimpanan: {jumlah_penyimpanan}\n"
                f"Kartu Grafis: {kartu_grafis}\n"
                f"Prosesor: {prosesor}\n"
                f"Ukuran Layar: {ukuran_layar}\n"
                f"Besar RAM: {besar_ram}\n"
                f"Ketahanan Baterai: {ketahanan_baterai}\n"
                f"Harga Terbaru: {harga_terbaru}\n"
                f"Harga Lama: {harga_lama}\n"
                f"Link Laptop: {link_laptop}")

    # Input dari pengguna
    nama_laptop = st.text_input('Silahkan isi nama laptop?', '')
    brand_laptop = st.selectbox('Silahkan pilih brand laptop', ('HP', 'Dell', 'asus', 'lenovo', 'acer'))
    tipe_penyimpanan = st.selectbox('Silahkan pilih Tipe Penyimpanan', ('SSD', 'HDD', 'eMMc'))
    jumlah_penyimpanan = st.number_input('Silahkan pilih Jumlah Penyimpanan')
    kartu_grafis = st.selectbox('Silahkan pilih Kartu Grafis', ('AMD Radeon', 'Intel UHD', 'NVDIA', 'Apple M2'))
    prosesor = st.selectbox('Silahkan pilih Prosesor', ('1920x1080', '1366x768'))
    ukuran_layar = st.selectbox('Silahkan pilih Ukuran Layar', ('12.5', '14.0', '15.6', '11.6'))
    besar_ram = st.number_input('Silahkan isi Besar RAM')
    ketahanan_baterai = st.number_input('Silahkan isi Ketahanan Baterai')
    harga_terbaru = st.number_input('Masukan Harga terbaru')
    harga_lama = st.number_input('Silahkan Masukan Harga Lama')
    link_laptop = st.text_input('Silahkan isi Link Laptop', '')

    konfirmasi = st.checkbox('Saya yakin data ingin disimpan')

    # Tombol "Tambah Data"
    if st.button("Tambah Data", type='primary') and konfirmasi:
        tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, besar_ram, ketahanan_baterai,
                    harga_terbaru, harga_lama, link_laptop)
        st.session_state.tambah_data = False  # Setel kembali ke False setelah pemrosesan
        st.info("Data berhasil disimpan.")


with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)




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
    