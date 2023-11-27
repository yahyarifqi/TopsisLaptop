import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page 

st.set_page_config(
    page_title="Rekomendasi Laptop",
    page_icon="👋",
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
    
st.subheader('Apakah Anda sedang mencari laptop sempurna yang memadukan \
         kinerja, gaya, dan inovasi sesuai keinginan Anda?', divider='rainbow')
st.write("**Tidak perlu bingung!** Kami hadir untuk menyederhanakan pencarian \
         dan membantu Anda menemukan laptop yang sesuai dengan kebutuhan \
           Anda.")

with st.container():
    image = Image.open('strixrog.png')
    st.image(image, caption='ASUS ROG STRIX')

st.header("Mengapa Menggunakan Layanan Kami?")

with st.container():
    st.subheader("1. Rekomendasi oleh Pakar Teknologi", divider='violet')
    st.write("Tim kami yang terdiri dari para ahli dan penggemar teknologi \
         dengan cermat meneliti dan menguji berbagai macam laptop untuk \
         memberikan Anda rekomendasi. Kebutuhan untuk pelajar, profesional, \
        atau penggemar game, kami siap membantu Anda.")
    
with st.container():
    st.subheader("2. Navigasi Mudah", divider='blue')
    st.write("Menemukan laptop yang tepat seharusnya tidak merepotkan. \
             *interface* kami yang mudah digunakan memungkinkan Anda \
             menyaring laptop berdasarkan preferensi Anda. \
             Kami mempermudah proses pengambilan keputusan Anda dalam membeli laptop")
    
with st.container():
    st.subheader("3. Detail Spesifikasi", divider='red')
    st.write("Untuk setiap data laptop yang ada, kami juga memberikan detail\
             spesifikasi untuk masing-masing laptop. Anda menjadi mudah untuk \
             membandingkan spesifikasi teknis dari pilihan-pilihan laptop.")

st.header("Laptop Sempurna Anda Menanti!")
st.write("Siap menemukan laptop yang sesuai dengan gaya hidup Anda? \
         Telusuri daftar pilihan kami, sistem rekomendasi kami, dan buatlah\
        keputusan pembelian laptop sempurna Anda hanya dengan sekali klik!")

col1, col2 = st.columns(2)

with col1:
    data_laptop = st.button("Data Laptop")
    image = Image.open('laptopmany.png')
    st.image(image)
    if data_laptop:
        switch_page("data_laptop")

with col2:
    sistem_rek = st.button("Rekomendasi Laptop")
    image = Image.open('rekom.png')
    st.image(image)
    if sistem_rek:
        switch_page("rekomendasi laptop")

