import streamlit as st
import pandas as pd

# Data contoh
data = {
    'ID': [1, 2, 3, 4],
    'Nama': ['Laptop A', 'Laptop B', 'Laptop C', 'Laptop D'],
    'Harga': [1000, 1200, 800, 1500],
}

df = pd.DataFrame(data)
st.dataframe(df)

# Kolom ID untuk mengedit data
selected_id = st.selectbox('Pilih ID untuk di edit', df['ID'])


if selected_id is not None:
    st.subheader(f"Hapus Data untuk ID {selected_id}")

    if st.button(f"Hapus Data untuk ID {selected_id}"):
        # Tampilkan pesan peringatan
        st.warning("Apakah Anda yakin ingin menghapus data ini?")

        # Tombol untuk konfirmasi "Ya"
        if st.button("Ya"):
            df = df[df['ID'] != selected_id]

            # Jalankan fungsi yang memerlukan waktu lama
            run_expensive_function()

            # Tampilkan DataFrame yang sudah diubah
            st.dataframe(df)
            st.success(f"Data untuk ID {selected_id} berhasil dihapus.")
        
        # Tombol untuk konfirmasi "Tidak"
        elif st.button("Tidak"):
            st.info(f"Data untuk ID {selected_id} tidak dihapus.")
            st.dataframe(df)
