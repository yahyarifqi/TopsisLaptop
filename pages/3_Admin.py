import pickle
from pathlib import Path

import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth 

st.set_page_config(page_title="Admin", page_icon="🔐")
st.markdown("# Admin")
st.sidebar.header("Admin")

names = ["Administrator"]
usernames = ["admin"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

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