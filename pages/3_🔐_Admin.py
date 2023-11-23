import pickle
from pathlib import Path
import pandas as pd
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
data_user = db.read_user()

st.set_page_config(page_title="Administrator", page_icon="🔐")
st.markdown("# Administrator")

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

    st.subheader("Baca Data Administrator")
    read_data_user = pd.DataFrame(data_user,columns=["Username","E-mail","Nama", "Password"])
    st.write(read_data_user)

    st.subheader("Tambah Data Administrator")
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
        st.success("Data Administrator baru berhasil ditambah: {}".format(create_name))
        st.rerun()

    st.subheader("Ubah Data Administrator")
    list_of_users = [i[0] for i in data_user]
    selected_user = st.selectbox("Data Administrator", list_of_users)
    user_result = db.get_user(selected_user)
        
    if user_result:
        current_username = user_result[0][0]
        current_email = user_result[0][1]
        current_name = user_result[0][2]
        current_password = user_result[0][3]

        col1, col2 = st.columns(2)
        with col1:
            update_username = st.text_input("Username", value=current_username)
            update_email = st.text_input("E-mail", value=current_email)
        with col2:
            update_name = st.text_input("Nama", value=current_name)
            update_password_list = []
            update_password = st.text_input("Password", type='password', value=current_password)
            update_password_list.append(update_password)
        
        if st.button("Ubah"):
            if(update_password==current_password):
                db.update_user(update_username, update_email, update_name, current_password, current_username, current_email, current_name, current_password)
                st.success("Data Administrator berhasil diubah: {}".format(update_username))
            else:
                update_hashed_passwords = stauth.Hasher(update_password_list).generate()
                update_hashed_passwords = update_hashed_passwords[0]
                db.update_user(update_username, update_email, update_name, update_hashed_passwords, current_username, current_email, current_name, current_password)
                st.success("Data Administrator berhasil diubah: {}".format(update_username))
            st.rerun()
        
        st.subheader("Hapus Data Administrator: {}".format(current_username))
        if st.button("Hapus", type='primary'):
            db.delete_user(current_username, current_email, current_name, current_password)
            st.success("Data Administrator berhasil dihapus: '{}'".format(current_username))
            st.rerun()