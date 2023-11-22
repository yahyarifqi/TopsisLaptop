import pickle
from pathlib import Path
import pandas as pd
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
data_user = db.get_user()

st.set_page_config(page_title="Admin", page_icon="🔐")
st.markdown("# Admin")

names = []
usernames = []
passwords = []
for data in data_user:
    data_names = data[2]
    data_usernames = data[0]
    data_passwords = data[3]

    names.append(data_names)
    usernames.append(data_usernames)
    passwords.append(data_passwords)

authenticator = stauth.Authenticate(names, usernames, passwords, cookie_name="spk", key="abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password salah!")

if authentication_status == None:
    st.warning("Masukkan username dan password!")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
	
    menu = ['Tambah/Create','Baca/Read','Ubah/Update','Hapus/Delete']
    choice = st.selectbox("CRUD Data Pengguna", menu)
    if choice=='Tambah/Create':
        st.subheader("Tambah Data Pengguna")
        col1, col2 = st.columns(2)
        with col1:
            create_username = st.text_input("Username")
            create_email = st.text_input("E-mail")
        with col2:
            create_name = st.text_input("Nama")
            create_password_list = []
            create_password = st.text_input("Password", type='password')
            create_password_list.append(create_password)
        if st.button("Tambah", type='primary'):
            hashed_passwords = stauth.Hasher(create_password_list).generate()
            hashed_passwords = hashed_passwords[0]
            db.create_user(create_username,create_email, create_name, hashed_passwords)
            st.success("User baru berhasil ditambah: {}".format(create_name))

    elif choice=='Baca/Read':
        st.subheader("Baca Data Pengguna")
        read_data_user = pd.DataFrame(data_user,columns=["Username","E-mail","Nama", "Password"])
        st.write(read_data_user)

    elif choice=='Ubah/Update':
        st.subheader("Ubah Data Pengguna")

    elif choice=='Hapus/Delete':
        st.subheader("Hapus Data Pengguna")