import streamlit as st
import pandas as pd
from topsis import Topsis

def calculate(data, crit):
    columns = [col for col in data.columns if col in crit.index]
    _evalMatrix = data[columns].to_numpy()
    print(_evalMatrix)

    _weight = []
    _impact = []

    for i in range(len(columns)):
        _weight.append(crit.loc[columns[i], 'weight'])
        _impact.append(crit.loc[columns[i], 'impact'])

    t = Topsis(_evalMatrix, _weight, _impact)
    t.calc()

    res = t.rank_to_worst_similarity()
    res.reverse()

    return res

def user_input(critTable):
    def addInput(row):
        row['weight'] = st.sidebar.slider('Bobot ' + row['text'], 0.0, 1.0, 1.0, 0.05)
        return row

    critTable = critTable.apply(addInput, axis=1)

    return critTable

def init():
    #Import tabel-tabel yang diperlukan
    data =  pd.read_csv('database.csv', encoding='unicode_escape')

    criteria = pd.read_csv('criteria.csv')
    criteria = criteria.set_index('criteria')

    subcrit = pd.read_csv('subcriteria.csv')

    category = pd.read_csv('categorization.csv',  encoding='unicode_escape')
    category['spesifikasi'] = category['spesifikasi'].map(lambda x: x.lower())
    category = category.drop_duplicates(subset=['spesifikasi']).set_index('spesifikasi')

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

    return data, criteria, matrixData

def write():

    st.write("""
    ## Rekomendasi laptop berdasarkan input user menggunakan TOPSIS

    di bawah adalah laptop yang direkomendasikan         
    """)

    data, criteria, matrixData = init()

    st.sidebar.header('Preferensi Bobot Pengguna')

    criteria = user_input(criteria)

    ranking = calculate(matrixData, criteria)

    st.write(data.iloc[ranking][['laptopName', 'newPrice', 'secondPrice']].reset_index(drop=True))

    return 0

write()


