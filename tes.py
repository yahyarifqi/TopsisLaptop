import streamlit as st

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

# Tombol "Tambah Data"
if st.button("Tambah Data", type='primary'):
    tambah_data(nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                kartu_grafis, prosesor, ukuran_layar, besar_ram, ketahanan_baterai,
                harga_terbaru, harga_lama, link_laptop)
