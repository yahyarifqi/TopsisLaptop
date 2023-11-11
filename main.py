import streamlit as st
import pandas as pd
from topsis import Topsis

#dicoba
import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import plotly_express as px
import time
from streamlit_option_menu import option_menu

#batas

#4. Manual Item Selection

if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None
    
selected4 = option_menu(None, ["Home", "Data Laptop", "Rekomendasi Laptop", 'Login'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    orientation="horizontal", manual_select=manual_select, key='menu_4')
# st.button(f"Move to Next {st.session_state.get('menu_option',1)}", key='switch_button')
selected4

# Logika untuk menampilkan konten sesuai dengan opsi yang dipilih
if selected4 == "Home":
    st.subheader("REKOMENDASI LAPTOP")
    st.write("---")
    st.text(
        "Pengen beli laptop tapi bingung mau milih yang mana?"
    )
    st.text(
        "Ayo cobain aplikasi Rekomendasi Laptop!"
    )
    # Tambahkan konten khusus untuk halaman Home di sini
elif selected4 == "Data Laptop":
    st.title("Halaman Upload")

    # Tambahkan konten khusus untuk halaman Upload di sini
elif selected4 == "Rekomendasi Laptop":
    #st.title("Halaman Tasks")
    def calculate(data, crit):
        columns = [col for col in data.columns if col in crit.index]
        _evalMatrix = data[columns].to_numpy()
        #print(_evalMatrix)

        _weight = []
        _impact = []

        #impact 1 means benefit impact while impact 0 means cost impact
        for i in range(len(columns)):
            _weight.append(crit.loc[columns[i], 'weight'])
            _impact.append(crit.loc[columns[i], 'impact'])

        t = Topsis(_evalMatrix, _weight, _impact)
        t.calc()

        res = t.rank_to_worst_similarity()
        res.reverse()

        return res

    def user_input(critTable):
        pricePref = {'newPrice':0, 'secondPrice':0}

        def addInput(row):
            print(row.name)
            row['weight'] = st.sidebar.slider('Bobot ' + row['text'], 0.0, 5.0, 1.0, 0.05)
            if row.name in pricePref.keys():
                pricePref[row.name] = st.sidebar.number_input('Preferensi ' + row['text'] + ' (Rupiah)', value=0, step=100000)
            return row

        critTable = critTable.apply(addInput, axis=1)

        return pricePref, critTable  

    def init():
        #Import tabel-tabel yang diperlukan
        data =  pd.read_csv('database.csv', encoding='unicode_escape')

        criteria = pd.read_csv('criteria.csv')
        criteria = criteria.set_index('criteria')

        subcrit = pd.read_csv('subcriteria.csv')

        category = pd.read_csv('categorization.csv',  encoding='unicode_escape')
        category['spesifikasi'] = category['spesifikasi'].map(lambda x: x.lower())
        category = category.drop_duplicates(subset=['spesifikasi']).set_index('spesifikasi')

        return data, criteria, subcrit, category

    def pre_process(data, criteria, subcrit, category, pricePref):
        #Normalisasi Data Harga
        for key in pricePref.keys():
            data[key] = data[key].map(lambda x: abs(x-pricePref[key]))

        #Mengubah data-data kategorikal ke dalam kategorinya masing-masing
        columns = [i for i in data.columns if i in category['criteria'].unique()]

        tempData = data.copy()
        tempData = tempData[[i for i in data.columns if i in criteria.index]]

        for col in columns:
            tempData[col] = data[col].map(lambda val:category.loc[val.lower(),'kelas'])

        #Mengubah data berbobot ke bobotnya masing-masing
        matrixData = tempData.copy()

        for col in tempData.columns:
            if criteria.loc[col, 'weighted']:
                _temp = subcrit[subcrit['criteria'] == col].set_index('value', drop=False)
                if criteria.loc[col,'type'] == 'discrete':
                    matrixData[col] = tempData[col].map(lambda x: _temp.loc[x,'weight'])   
                else:
                    def process_num(value):
                        res = 0
                        for index,row in _temp.iterrows():
                            if value >= float(row['value']):
                                res = row['weight']  
                        return res
                    
                    matrixData[col] = tempData[col].map(process_num)
        return matrixData

    def write():

        st.write("""
        ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

        Di bawah adalah daftar laptop yang tersedia      
        """)

        data, criteria, subcrit, category = init()

        st.sidebar.header('Preferensi Bobot Pengguna')

        pricePref, criteria = user_input(criteria)

        print(pricePref)

        matrixData = pre_process(data.copy(), criteria, subcrit, category, pricePref)

        st.write(data)

        ranking = calculate(matrixData, criteria)

        st.write("Di bawah adalah rekomendasi laptop yang kami berikan")
        st.write(data.iloc[ranking][['laptopName', 'newPrice', 'secondPrice']].reset_index(drop=True))

        return 0

    write()
    # Tambahkan konten khusus untuk halaman Tasks di sini
elif selected4 == "Login":
    st.title("Halaman Settings")
    # Tambahkan konten khusus untuk halaman Settings di sini

