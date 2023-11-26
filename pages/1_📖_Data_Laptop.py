import pandas as pd
import streamlit as st
from dbmanagement import DbManagement
from streamlit.components.v1 import html


db = DbManagement('laptopsis.db')

st.set_page_config(page_title="Data Laptop", page_icon="📖")
st.markdown("# Data Laptop")

dataLaptop = db.get_laptop_data()
criteria = db.get_criteria().set_index('ID')
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

    def edit_data(laptop_id, nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                  kartu_grafis, prosesor, ukuran_layar, resolusi_layar, ram, ketahanan_baterai, bobot,
                  harga_terbaru, harga_lama, link_laptop):
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

        if (laptop_id):
            db.update_laptop(laptop_id,link_laptop, nama_laptop, discrete_criteria, numeric_criteria)

        
    # st.dataframe(df)

# Kolom ID untuk mengedit data
    selected_id = st.selectbox('Pilih ID untuk di edit', dataLaptop.index)

    if 'update' not in st.session_state: st.session_state['update'] = False

    # Tampilkan form untuk mengedit data jika ID dipilih
    if st.button("Edit Data") and selected_id:
        st.session_state['update'] = True
    
    if st.session_state['update']:
        st.subheader(f"Edit Data untuk ID {selected_id}")
        editedRow = dataLaptop.loc[selected_id]
        
        def select_discrete_criteria(critIndex, data):
            arr = db.read_categorization_from_criteria(critIndex)
            return st.selectbox('Silahkan pilih ' + criteria.loc[critIndex]['text'], arr, 
                                list(zip(*arr))[1].index(data[criteria.loc[critIndex]['criteria']]), 
                                format_func=lambda x: x[1],)

        with st.form(key='edit_form'):
            nama_laptop = st.text_input('Silahkan isi nama laptop', editedRow['laptopName'])
            link_laptop = st.text_input('Silahkan isi Link Laptop', editedRow['detailLink'])
            brand_laptop = select_discrete_criteria(1, editedRow)
            tipe_penyimpanan = select_discrete_criteria(5, editedRow)
            jumlah_penyimpanan  = st.number_input('Silahkan isi Jumlah Penyimpanan (GB)', value=editedRow['storage'])
            kartu_grafis = select_discrete_criteria(7, editedRow)
            prosesor = select_discrete_criteria(4, editedRow)
            ukuran_layar = st.number_input('Silahkan isi Ukuran Layar (inci)', value=editedRow['screenSize'])
            resolusi_layar = select_discrete_criteria(3, editedRow)
            ram = st.number_input('Silahkan isi besar RAM (GB)', value=editedRow['ram'])
            ketahanan_baterai = st.number_input('Silahkan isi Ketahanan Baterai (Jam)', value=editedRow['durability'])
            bobot = st.number_input('Silakan isi bobot dari laptop (Kg)', value=editedRow['weight'])
            harga_terbaru = st.number_input('Masukan Harga terbaru (Rupiah)', value=editedRow['newPrice'])
            harga_lama = st.number_input('Silahkan Masukan Harga Bekas (Rupiah)', value=editedRow['secondPrice'])

            submitted = st.form_submit_button('Simpan Perubahan')
            
        if submitted:
            edit_data(selected_id, nama_laptop, brand_laptop, tipe_penyimpanan, jumlah_penyimpanan,
                    kartu_grafis, prosesor, ukuran_layar, resolusi_layar, ram, ketahanan_baterai, bobot,
                    harga_terbaru, harga_lama, link_laptop)
            st.success(f"Data untuk ID {selected_id} berhasil diubah.")
            st.session_state['update'] = False
            
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
            
        

