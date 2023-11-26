import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from topsis import Topsis
import streamlit_authenticator as stauth
from dbmanagement import DbManagement
from streamlit.components.v1 import html
import time


db = DbManagement('laptopsis.db')

st.set_page_config(page_title="Data Laptop", page_icon="📖")
st.markdown("# Data Laptop")

st.write("""
    ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

    Di bawah adalah daftar laptop yang tersedia      
    """)

dataLaptop = db.get_laptop_data()
st.write(dataLaptop)

tab1, tab2= st.tabs(["CREATE", "UPDATE"])

with tab1:

    def tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, resolusi_layar, ram, ketahanan_baterai, bobot,
                    harga_terbaru, harga_lama, link_laptop):
        # Di sini, Anda dapat menambahkan logika untuk menyimpan data ke database atau melakukan operasi lainnya
        discrete_criteria = [
            (1, brand_laptop[0]),
            (3, resolusi_layar[0]),
            (4, prosesor[0]),
            (5, tipe_penyimpanan[0]),
            (7, kartu_grafis[0])
        ]
        numeric_criteria = [
            (2, ukuran_layar),
            (6, jumlah_penyimpanan),
            (8, bobot),
            (9, ketahanan_baterai),
            (10, harga_terbaru),
            (11, harga_lama),
            (12, ram)
        ]
        
        nama_laptop = '-' if not nama_laptop else nama_laptop
        link_laptop = '-' if not link_laptop else link_laptop

        db.create_laptop(nama_laptop, link_laptop, discrete_criteria, numeric_criteria)

    # Input dari pengguna
    nama_laptop = st.text_input('Silahkan isi nama laptop', '')
    link_laptop = st.text_input('Silahkan isi Link Laptop', '')
    brand_laptop = st.selectbox('Silahkan pilih brand laptop', db.read_categorization_from_criteria(1), format_func=lambda x: x[1])
    tipe_penyimpanan = st.selectbox('Silahkan pilih Tipe Penyimpanan', db.read_categorization_from_criteria(5), format_func= lambda x:x[1])
    jumlah_penyimpanan = st.number_input('Silahkan isi Jumlah Penyimpanan (GB)')
    kartu_grafis = st.selectbox('Silahkan pilih Kartu Grafis', db.read_categorization_from_criteria(7), format_func= lambda x:x[1])
    prosesor = st.selectbox('Silahkan pilih Prosesor', db.read_categorization_from_criteria(4), format_func= lambda x:x[1])
    ukuran_layar = st.number_input('Silahkan isi Ukuran Layar (inci)')
    resolusi_layar = st.selectbox('Silakan pilih resolusi layar', db.read_categorization_from_criteria(3), format_func= lambda x:x[1])
    ram = st.number_input('Silahkan isi besar RAM (GB)')
    ketahanan_baterai = st.number_input('Silahkan isi Ketahanan Baterai (Jam)')
    bobot = st.number_input('Silakan isi bobot dari laptop (Kg)')
    harga_terbaru = st.number_input('Masukan Harga terbaru (Rupiah)')
    harga_lama = st.number_input('Silahkan Masukan Harga Bekas (Rupiah)')

    konfirmasi = st.checkbox('Saya yakin data ingin disimpan')

    # Tombol "Tambah Data"
    if st.button("Tambah Data", type='primary') and konfirmasi:
        tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, resolusi_layar, ram, ketahanan_baterai, bobot,
                    harga_terbaru, harga_lama, link_laptop)
        st.session_state.tambah_data = False  # Setel kembali ke False setelah pemrosesan
        st.info("Data berhasil disimpan.")


with tab2:
    data ={ 
        'ID' : [1,2,3,4],
        'Nama Laptop' : ['ASUS Laptop M409DA', 'ASUS Laptop X441UB', 'Apple Macbook Air M1 2020', 'Lenovo Legion 5 Pro' ],
        'Brand Laptop' : ['HP', 'Dell', 'asus', 'lenovo'],
        'Tipe Penyimpanan' : ['SSD', 'HDD', 'eMMc', 'SSD'],
        'Jumlah Penyimpanan' : [512, 256, 512, 160],
        'Kartu Grafis' : ['Integrated Intel UHD Graphics', 'Intel HD Graphics 4000', 'NVIDIA Quadro NVS 3100M', 'Intel® Integrated'],
        'Prosesor' :  ['Intel Core i3-7020U', 'Intel Core i5-10300H', 'Intel Core i5', 'M2 Chip CPU 8-core GPU 8-core'],
        'Ukuran Layar' : ['1920x1080', '2560x1664', '1366x768', '1366x768'],
        'Ram' : [4, 8, 7, 3],
        'Ketahanan Baterai' : [134, 16, 10, 11],
        'Harga Terbaru': [4399000, 13779000, 1350000, 3999000],
        'Harga Bekas' :[1700000, 16499999, 1599999, 3000000],
        'Link Laptop' :['http://localhost:8506/Data_Laptop', 'http://localhost:8506/Data_Laptop', 'http://localhost:8506/Data_Laptop', 'http://localhost:8506/Data_Laptop'],
    }
    
    #  Buat DataFrame
    df = pd.DataFrame(data)

    def edit_data(id_to_edit, new_nama_laptop, new_brand_laptop, new_tipe_penyimpanan, new_jumlah_penyimpanan, new_kartu_grafis, new_prosesor, new_ukuran_layar, new_ram, new_ketahanan_baterai, new_harga_terbaru, new_harga_bekas, new_link_laptop):
            index_to_edit = df.index[df['ID'] ==  id_to_edit].tolist([0])
            df.at[index_to_edit, 'Nama Laptop'] = new_nama_laptop
            df.at[index_to_edit, 'Brand Laptop'] = new_brand_laptop
            df.at[index_to_edit, 'Tipe Penyimpanan'] = new_tipe_penyimpanan
            df.at[index_to_edit, 'Jumlah Penyimpanan'] = new_jumlah_penyimpanan
            df.at[index_to_edit, 'Kartu Grafis'] = new_kartu_grafis
            df.at[index_to_edit, 'Prosesor'] = new_prosesor
            df.at[index_to_edit, 'Ukuran Layar'] = new_ukuran_layar
            df.at[index_to_edit, 'Ram'] = new_ram
            df.at[index_to_edit, 'Ketahanan Batrei'] = new_ketahanan_baterai
            df.at[index_to_edit, 'Harga Terbaru'] = new_harga_terbaru
            df.at[index_to_edit, 'Harga Bekas'] = new_harga_bekas
            df.at[index_to_edit, 'Link Laptop'] = new_link_laptop
        
    # st.dataframe(df)

# Kolom ID untuk mengedit data
    selected_id = st.selectbox('Pilih ID untuk di edit', dataLaptop.index)

    # Tampilkan form untuk mengedit data jika ID dipilih
    if st.button("Edit Data") and selected_id:
        st.subheader(f"Edit Data untuk ID {selected_id}")
        row_to_edit = df[df['ID'] == selected_id].iloc[0]
        
        with st.form(key='edit_form'):
            new_nama_laptop = st.text_input('Nama Laptop:', row_to_edit['Nama Laptop'])
            new_brand_laptop = st.selectbox('Silahkan pilih brand laptop', df['Brand Laptop'].unique(), index=df['Brand Laptop'].unique().tolist().index(row_to_edit['Brand Laptop']))
            new_tipe_penyimpanan = st.selectbox('Silahkan pilih Tipe Penyimpanan', df['Tipe Penyimpanan'].unique(), index=df['Tipe Penyimpanan'].unique().tolist().index(row_to_edit['Tipe Penyimpanan']))
            new_jumlah_penyimpanan = st.number_input('Silahkan pilih Jumlah Penyimpanan', float(row_to_edit['Jumlah Penyimpanan']))
            new_kartu_grafis = st.selectbox('Silahkan pilih Kartu Grafis', df['Kartu Grafis'].unique(), index=df['Kartu Grafis'].unique().tolist().index(row_to_edit['Kartu Grafis']))
            new_prosesor = st.selectbox('Silahkan pilih Prosesor', df['Prosesor'].unique(), index=df['Prosesor'].unique().tolist().index(row_to_edit['Prosesor']))
            new_ukuran_layar = st.selectbox('Silahkan pilih Ukuran Layar', df['Ukuran Layar'].unique(), index=df['Ukuran Layar'].unique().tolist().index(row_to_edit['Ukuran Layar']))
            new_ram = st.number_input('Silahkan isi Besar RAM', float(row_to_edit['Ram']))
            new_ketahanan_baterai = st.number_input('Silahkan isi Ketahanan Baterai', float(row_to_edit['Ketahanan Baterai']))
            new_harga_terbaru = st.number_input('Masukan Harga terbaru', float(row_to_edit['Harga Terbaru']))
            new_harga_bekas = st.number_input('Silahkan Masukan Harga Lama', float(row_to_edit['Harga Bekas']))
            new_link_laptop = st.text_input('Silahkan isi Link Laptop', row_to_edit['Link Laptop'])
            submitted = st.form_submit_button('Simpan Perubahan')
            
        if submitted:
            edit_data(selected_id, new_nama_laptop, new_brand_laptop, new_tipe_penyimpanan, new_jumlah_penyimpanan, new_kartu_grafis, new_prosesor, new_ukuran_layar, new_ram, new_ketahanan_baterai, new_harga_terbaru, harga_bekas, new_link_laptop)
            st.success(f"Data untuk ID {selected_id} berhasil diubah.")
            
# HAPUS
    # Tampilkan konfirmasi penghapusan jika ID dipilih
    if 'delete' not in st.session_state: st.session_state['delete'] = False
    if 'warning' not in st.session_state: st.session_state['warning'] = False
    if selected_id is not None:
        
        if st.button(f"Hapus Data"):
            # Tampilkan pesan peringatan
            st.session_state['warning'] = True

        if st.session_state['warning']:
            st.warning("Apakah Anda yakin ingin menghapus data ini?")
            if st.button("Ya"):
                st.session_state['warning'] = False
                st.session_state['delete'] = True
                
        if st.session_state['delete']:
            db.delete_laptop(selected_id)
            st.session_state['delete'] = False
            st.rerun()
            
        

