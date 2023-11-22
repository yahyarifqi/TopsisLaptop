import pandas as pd
import sqlite3

class DbManagement():
    
    def __init__(self, database):
        self.connection = sqlite3.connect(database=database, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def get_laptop_data(self, for_topsis = False):
        statement1 = ''.join(['''
        SELECT laptop.laptopName, criteria.criteria, ''',
        'sub_criteria.weight as specification' if for_topsis else 'categorization.specification','''
        FROM discrete_criteria LEFT OUTER JOIN laptop ON discrete_criteria.laptop = laptop.ID
        LEFT OUTER JOIN criteria ON discrete_criteria.criteria = criteria.ID
        LEFT OUTER JOIN categorization ON discrete_criteria.category = categorization.ID
        ''','LEFT OUTER JOIN sub_criteria ON categorization.class = sub_criteria.ID' if for_topsis else ''])

        statement2 = '''
        SELECT laptop.laptopName, criteria.criteria, numeric_criteria.value as specification
        FROM numeric_criteria LEFT OUTER JOIN laptop ON numeric_criteria.laptop = laptop.ID
        LEFT OUTER JOIN criteria ON numeric_criteria.criteria = criteria.ID
        '''
        result1 = pd.read_sql_query(statement1, self.connection)
        result2 = pd.read_sql_query(statement2, self.connection)

        result = pd.concat([result1,result2], ignore_index=True)

        result = result.drop_duplicates(subset=['laptopName','criteria'])
        result = result.pivot(index='laptopName', columns='criteria', values='specification').reset_index()
        return result

    def get_criteria(self):
        statement = '''
        SELECT * from criteria
        '''
        result = pd.read_sql_query(statement, self.connection)
        return result
    
    def get_sub_criteria(self):
        statement = '''
        SELECT criteria.criteria, weight.value, weight.weight from weight
        LEFT OUTER JOIN criteria ON weight.criteria = criteria.ID
        '''

        result = pd.read_sql_query(statement, self.connection)
        return result
    
    def get_user(self):
        statement = '''
        SELECT * from user
        '''

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def __del__(self):
        self.connection.close()



