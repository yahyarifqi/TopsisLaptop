import pickle
from pathlib import Path

import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
from dbmanagement import DbManagement

db = DbManagement('laptopsis.db')
data_user = db.get_user()

st.set_page_config(page_title="Admin", page_icon="🔐")
st.markdown("# Admin")
st.sidebar.header("Admin")

names = []
usernames = []
passwords = []
for data in data_user:
    st.write(data)
    data_names = data[2]
    data_usernames = data[0]
    data_passwords = data[3]

    names.append(data_names)
    usernames.append(data_usernames)
    passwords.append(data_passwords)
    st.write(data_names)

st.write(names)
st.write(usernames)
st.write(passwords)

# # load hashed passwords
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, passwords, cookie_name="spk", key="abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.write("""
             ## Laman Admin     
             """)