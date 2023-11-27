import streamlit as st
import pandas as pd
from topsis import Topsis
from dbmanagement import DbManagement
db = DbManagement('laptopsis.db')

def calculate(data, crit):
    columns = [col for col in data.columns if col in crit.index]
    _evalMatrix = data[columns].to_numpy()

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
        with col1:
            if row.name in ['brandName', 'screenSize', 'screenResolution', 'processors', 'diskType', 'storage', 'graphicCard']:
                row['weight'] = st.slider('Bobot ' + row['text'], 0.0, 5.0, 1.0, 0.05)
        with col2:
                if row.name in ['ram', 'weight', 'durability', 'newPrice', 'secondPrice']:
                    row['weight'] = st.slider('Bobot ' + row['text'], 0.0, 5.0, 1.0, 0.05)
                if row.name in pricePref.keys():
                    pricePref[row.name] = st.number_input('Preferensi ' + row['text'] + ' (Rupiah)', value=0, step=100000)
        return row

    critTable = critTable.apply(addInput, axis=1)

    return pricePref, critTable  

def init():
    #Import tabel-tabel yang diperlukan
    db = DbManagement('laptopsis.db')
    data =  db.get_laptop_data(for_topsis=True)

    criteria = db.get_criteria()
    criteria = criteria.set_index('criteria')

    subcrit = db.get_sub_criteria()

    return data, criteria, subcrit

def pre_process(data, criteria, subcrit, pricePref):
    #Normalisasi Data Harga
    for key in pricePref.keys():
        data[key] = data[key].map(lambda x: abs(x-pricePref[key]))

    matrixData = data.copy()

    for col in [i for i in data.columns if i in criteria.index]:
        if criteria.loc[col, 'weighted']:
            _temp = subcrit[subcrit['criteria'] == col].set_index('value', drop=False)
            if criteria.loc[col,'type'] == 'numeric':
            #     matrixData[col] = data[col].map(lambda x: _temp.loc[x,'weight'])   
            # else:
                def process_num(value):
                    res = 0
                    for index,row in _temp.iterrows():
                        if value >= float(row['value']):
                            res = row['weight']  
                    return res
                
                matrixData[col] = data[col].map(process_num)
    return matrixData

st.set_page_config(page_title="Rekomendasi Laptop", page_icon="🛒")
st.markdown("# Rekomendasi Laptop")
st.write("Silahkan masukkan bobot preferensi laptop Anda")
col1, col2 = st.columns(2)

data, criteria, subcrit = init()

pricePref, criteria = user_input(criteria)
matrixData = pre_process(data.copy(), criteria, subcrit, pricePref)
ranking = calculate(matrixData, criteria)

st.write("Di bawah adalah rekomendasi laptop yang kami berikan")
st.write(data.iloc[ranking][['laptopName', 'newPrice', 'secondPrice']].reset_index(drop=True))