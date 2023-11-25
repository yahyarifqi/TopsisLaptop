# import pickle
# from pathlib import Path
# import pandas as pd
# import streamlit as st
# from topsis import Topsis
# import streamlit_authenticator as stauth
# from dbmanagement import DbManagement

# db = DbManagement('laptopsis.db')
# data_weight = db.read_weight()

# st.markdown("# DATA WEIGHT")

# w_id = []
# criteria= []
# value = []
# weight = []
# for data in data_weight:
#     data_w_id = data[0]
#     data_criteria = data[1]
#     data_value = data[2]
#     data_weight = data[3]

#     w_id.append(data_w_id)
#     criteria.append(data_criteria)
#     value.append(data_value)
#     weight.append(data_weight)

# st.subheader("BACA DATA Weight")
# read_data_weight =pd.DataFrame(data_weight, columns=["id","criteria","value", "weight"])
# st.write(read_data_weight)
        
# st.subheader("Tambah Data Weight")
# col1, col2, col3 = st.columns(3)
# with col1:
#     create_id = st.text_input("id")
#     create_criteria = st.text_input("criteria")
# with col2:
#     create_value = st.text_input("value")
#     create_weight = st.text_input("weight")
# if st.button("Tambah", type='primary'):
#     # Lakukan validasi input atau operasi lain jika diperlukan
#     db.create_weight(create_id, create_criteria, create_value, create_weight)
#     st.success("Data Weight baru berhasil ditambah: id{}, criteria={}, value={}, weight={}".format(
#         create_id, create_criteria, create_value, create_weight))
#     st.rerun()

# st.subheader("Ubah Data Weight")
# list_of_categrizations = [i[0] for i in data_weight]
# selected_weight = st.selectbox("Data Categorization", list_of_categrizations)
# weight_result = db.get_weight(selected_weight)

# # Tampilkan data kategorisasi yang dipilih
# if weight_result:
#     current_id = weight_result[0][0]
#     current_criteria = weight_result [0][1]
#     current_value = weight_result[0][2]
#     current_weight = weight_result[0][3]


#     st.subheader("Form Ubah Data Weight")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         update_id = st.text_input("ID", value=current_id)
#         update_criteria = st.text_input("Criteria", value=current_criteria)
#     with col2:
#         update_value = st.text_input("Value", value=current_value)
#     with col3:
#         update_weight = st.text_input("weight", value=current_weight)

#     if st.button("Ubah", type='primary'):
#         # Lakukan validasi input atau operasi lain jika diperlukan
#         db.update_weight(update_id, update_criteria, update_value, update_weight, current_id, current_criteria, current_value, current_weight)
#         st.success("Data Weight berhasil diubah: ID={}, Criteria={}, Value={}, Weight={}".format(update_id, update_criteria, update_value, update_weight))
#         st.rerun()
# else:
#     st.warning("Data Weight dengan ID {} tidak ditemukan.".format(update_id))

# st.subheader("Hapus Data Weight: {}".format(current_id))
# if st.button("Hapus", type='primary'):
#     db.delete_weight(current_id, current_criteria, current_value, current_weight)
#     st.success("Data Weight berhasil dihapus: '{}'".format(current_id))
#     st.rerun()