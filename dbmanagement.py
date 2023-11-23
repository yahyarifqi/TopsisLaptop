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
    
    def read_user(self):
        statement = '''
        SELECT * from user
        '''

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    
    def create_user(self, create_username, create_email, create_name, create_password):
        statement = '''
        INSERT INTO  user(username,email,name,password) VALUES (?,?,?,?)
        '''

        result = self.cursor.execute(statement, (create_username, create_email, create_name, create_password))
        result = self.connection.commit()
        return result
    
    def get_user(self, selected_user):
        statement = '''
        SELECT * from user where username = '{}'
        '''.format(selected_user)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    
    def update_user(self, update_username, update_email, update_name, update_hashed_password, current_username, current_email, current_name, current_password):
        statement = '''
        update user set username=?, email=?, name=?, password=? where username=? and email=? and name=? and password=?
        '''

        result = self.cursor.execute(statement, (update_username, update_email, update_name, update_hashed_password, current_username, current_email, current_name, current_password))
        result = self.connection.commit()
        return result
    
    def delete_user(self, current_username, current_email, current_name, current_password):
        statement = '''
        delete from user where username=? and email=? and name=? and password=?
        '''

        result = self.cursor.execute(statement, (current_username, current_email, current_name, current_password))
        result = self.connection.commit()
        return result


    # DATA CAtegorization

    
    def read_categorization(self):
        statement = '''
        SELECT * from categorization
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_categorization(self, create_id, create_specification, create_criteria, create_class):
        statement = ''' 
        INSERT INTO categorization(id,specification,criteria,class)
        VALUES (?,?,?,?)
        '''

        result = self.cursor.execute(statement, (create_id, create_specification, create_criteria, create_class))
        result = self.connection.commit()
        return result
    
    def get_categorization(self, selected_categorization):
        statement = '''
        SELECT * FROM categorization where id = '{}'
        '''.format(selected_categorization)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def update_categorization(self, update_id, update_specification, update_criteria, update_class, current_id, current_specification, current_criteria, current_class):
        statement = '''
        update categorization set id=?, specification=?, criteria=?, class=? where id=? and specification=? and criteria=? and class=?
        '''

        result = self.cursor.execute(statement, (update_id, update_specification, update_criteria, update_class, current_id, current_specification,current_criteria, current_class))
        result = self.connection.commit()
        return result

    def delete_categorization(self, current_id, current_specification, current_criteria, current_class):
        statement = '''
        delete from categorization where id=? and specification=? and criteria=? and class=?
        '''

        result = self.cursor.execute(statement, (current_id, current_specification, current_criteria, current_class))
        result = self.connection.commit()
        return result

    def __del__(self):
        self.connection.close()



