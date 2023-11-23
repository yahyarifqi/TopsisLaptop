import streamlit as st

st.set_page_config(
    page_title="Rekomendasi Laptop",
    page_icon="📈",
    layout="wide",
)

st.sidebar.success("Silahkan memilih laman yang ingin dituju.")

try:
    if st.session_state["authentication_status"]:
        st.write(f'# Selamat Datang *{st.session_state["name"]}* di Aplikasi Rekomendasi Laptop! 👋')
    else:
        st.write("# Selamat Datang di Aplikasi Rekomendasi Laptop! 👋")
except:
    st.write("# Selamat Datang di Aplikasi Rekomendasi Laptop! 👋")