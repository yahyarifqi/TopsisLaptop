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

st.write(db.get_laptop_data())

tab1, tab2= st.tabs(["CREAT", "UPDATE"])

with tab1:

    def tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, ram, ketahanan_baterai,
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
                f"Besar RAM: {ram}\n"
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
    ram = st.number_input('Silahkan isi Besar RAM')
    ketahanan_baterai = st.number_input('Silahkan isi Ketahanan Baterai')
    harga_terbaru = st.number_input('Masukan Harga terbaru')
    harga_lama = st.number_input('Silahkan Masukan Harga Lama')
    link_laptop = st.text_input('Silahkan isi Link Laptop', '')

    konfirmasi = st.checkbox('Saya yakin data ingin disimpan')

    # Tombol "Tambah Data"
    if st.button("Tambah Data", type='primary') and konfirmasi:
        tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, ram, ketahanan_baterai,
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
    selected_id = st.selectbox('Pilih ID untuk di edit', df['ID'])

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
    if selected_id is not None:
        st.subheader(f"Hapus Data untuk ID {selected_id}")
        
        if st.button(f"Hapus Data untuk ID {selected_id}"):
            # Tampilkan pesan peringatan
            st.warning("Apakah Anda yakin ingin menghapus data ini?")
            if st.button("Ya"):
                df = df[df['ID'] != selected_id]
                # Jalankan fungsi yang memerlukan waktu lama
                run_expensive_function()
            
                st.dataframe(df)
                st.success(f"Data untuk ID {selected_id} berhasil dihapus.")
            # Tombol untuk konfirmasi "Tidak"
            elif st.button("Tidak"):
                st.info(f"Data untuk ID {selected_id} tidak dihapus.")
                st.dataframe(df)


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
    












#     try:
#         df = pd.DataFrame(data)
#         print(df)
#     except Exception as e:
#         print(f"Error: {e}")

#     def edit_data(id_to_edit, new_nama_laptop, new_brand_laptop, new_tipe_penyimpanan, new_jumlah_penyimpanan, new_kartu_grafis, new_prosesor, new_ukuran_layar, new_ram, new_ketahanan_baterai, new_harga_terbaru, new_harga_bekas, new_link_laptop):
#             index_to_edit = df.index[df['ID'] ==  id_to_edit].tolist([0])
#             df.at[index_to_edit, 'Nama Laptop'] = new_nama_laptop
#             df.at[index_to_edit, 'Brand Laptop'] = new_brand_laptop
#             df.at[index_to_edit, 'Tipe Penyimpanan'] = new_tipe_penyimpanan
#             df.at[index_to_edit, 'Jumlah Penyimpanan'] = new_jumlah_penyimpanan
#             df.at[index_to_edit, 'Kartu Grafis'] = new_kartu_grafis
#             df.at[index_to_edit, 'Prosesor'] = new_prosesor
#             df.at[index_to_edit, 'Ukuran Layar'] = new_ukuran_layar
#             df.at[index_to_edit, 'Ram'] = new_ram
#             df.at[index_to_edit, 'Ketahanan Batrei'] = new_ketahanan_baterai
#             df.at[index_to_edit, 'Harga Terbaru'] = new_harga_terbaru
#             df.at[index_to_edit, 'Harga Bekas'] = new_harga_bekas
#             df.at[index_to_edit, 'Link Laptop'] = new_link_laptop
        
#     st.dataframe(df)

# # Kolom ID untuk mengedit data
#     selected_id = st.selectbox('Pilih ID untuk di edit', df['ID'])

#     # Tampilkan form untuk mengedit data jika ID dipilih
#     if st.button("Edit Data") and selected_id:
#         st.subheader(f"Edit Data untuk ID {selected_id}")
#         row_to_edit = df[df['ID'] == selected_id].iloc[0]
        
#         with st.form(key='edit_form'):
#             new_nama_laptop = st.text_input('Nama Laptop:', row_to_edit['Nama Laptop'])
#             new_brand_laptop = st.selectbox('Silahkan pilih brand laptop', row_to_edit['Brand Laptop'])
#             new_tipe_penyimpanan = st.selectbox('Silahkan pilih Tipe Penyimpanan', row_to_edit['Tipe Penyimpanan'])
#             new_jumlah_penyimpanan = st.number_input('Silahkan pilih Jumlah Penyimpanan', float(row_to_edit['Jumlah Penyimpanan']))
#             new_kartu_grafis = st.selectbox('Silahkan pilih Kartu Grafis', row_to_edit['Kartu Grafis'])
#             new_prosesor = st.selectbox('Silahkan pilih Prosesor', row_to_edit['Prosesor'])
#             new_ukuran_layar = st.selectbox('Silahkan pilih Ukuran Layar', row_to_edit['Ukuran Layar'])
#             new_ram = st.number_input('Silahkan isi Besar RAM', float(row_to_edit['Ram']))
#             new_ketahanan_baterai = st.number_input('Silahkan isi Ketahanan Baterai', float(row_to_edit['Ketahanan Baterai']))
#             new_harga_terbaru = st.number_input('Masukan Harga terbaru', float(row_to_edit['Harga Terbaru']))
#             new_harga_bekas = st.number_input('Silahkan Masukan Harga Lama', float(row_to_edit['Harga Bekas']))
#             new_link_laptop = st.text_input('Silahkan isi Link Laptop', row_to_edit['Link Laptop'])
#             submitted = st.form_submit_button('Simpan Perubahan')
            
#         if submitted:
#                 edit_data(selected_id, new_nama_laptop, new_brand_laptop, new_tipe_penyimpanan, new_jumlah_penyimpanan, new_kartu_grafis, new_prosesor, new_ukuran_layar, new_ram, new_ketahanan_baterai, new_harga_terbaru, harga_bekas, new_link_laptop)
#                 st.success(f"Data untuk ID {selected_id} berhasil diubah.")
