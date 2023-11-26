import pandas as pd
import sqlite3

class DbManagement():
    
    def __init__(self, database):
        self.connection = sqlite3.connect(database=database, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def get_laptop_data(self, for_topsis = False):
        statement1 = ''.join(['''
        SELECT laptop.ID, laptop.laptopName, laptop.detailLink, criteria.criteria, ''',
        'sub_criteria.weight as specification' if for_topsis else 'categorization.specification','''
        FROM discrete_criteria LEFT OUTER JOIN laptop ON discrete_criteria.laptop = laptop.ID
        LEFT OUTER JOIN criteria ON discrete_criteria.criteria = criteria.ID
        LEFT OUTER JOIN categorization ON discrete_criteria.category = categorization.ID
        ''','LEFT OUTER JOIN sub_criteria ON categorization.class = sub_criteria.ID' if for_topsis else ''])

        statement2 = '''
        SELECT laptop.ID, laptop.laptopName, laptop.detailLink, criteria.criteria, numeric_criteria.value as specification
        FROM numeric_criteria LEFT OUTER JOIN laptop ON numeric_criteria.laptop = laptop.ID
        LEFT OUTER JOIN criteria ON numeric_criteria.criteria = criteria.ID
        '''
        result1 = pd.read_sql_query(statement1, self.connection)
        result2 = pd.read_sql_query(statement2, self.connection)

        result = pd.concat([result1,result2], ignore_index=True)

        result = result.drop_duplicates(subset=['ID','laptopName','criteria'])
        result = result.pivot(index=['ID','laptopName', 'detailLink'], columns='criteria', values='specification').reset_index().set_index('ID')

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

#region unused_code
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

        # DATA CRITERIA

    def read_criteria(self):
        statement = '''
        SELECT * from criteria
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_criteria(self, create_id, create_criteria, create_text, create_weight, create_impact, create_type, create_weighted):
        statement = ''' 
        INSERT INTO criteria(id,criteria,text,weight,impact,type,weighted)
        VALUES (?,?,?,?,?,?,?)
        '''

        result = self.cursor.execute(statement, (create_id, create_criteria, create_text, create_weight, create_impact, create_type, create_weighted))
        result = self.connection.commit()
        return result
    
    def get_Criteria(self, selected_Criteria):
        statement = '''
        SELECT * FROM criteria where id = '{}'
        '''.format(selected_Criteria)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def update_criteria(self, update_id, update_criteria, update_text, update_weight, update_impact, update_type, update_weighted,
                            current_id, current_criteria, current_text, current_weight, current_impact, current_type, current_weighted):
        statement = '''
        update criteria set id=?, criteria=?, text=?, weight=?, impact=?, type=?, weighted=?
                        where id=? and criteria=? and text=? and weight=? and impact=? and type=? and weighted=?
        '''

        result = self.cursor.execute(statement, (update_id, update_criteria, update_text, update_weight, update_impact, update_type, update_weight,
                                                current_id, current_criteria, current_text, current_weight, current_impact, current_type, current_weighted))
        result = self.connection.commit()
        return result

    def delete_criteria(self,  current_id, current_criteria, current_text, current_weight, current_impact, current_type, current_weighted):
        statement = '''
        delete from criteria where id=? and criteria=? and text=? and weight=? and impact=? and type=? and weighted=?
        '''

        result = self.cursor.execute(statement, (current_id, current_criteria, current_text, current_weight, current_impact, current_type, current_weighted))
        result = self.connection.commit()
        return result

    # DATA DISCRITE CRITERIA

    def read_discrete_criteria(self):
        statement = '''
        SELECT * from discrete_criteria
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_discrete_criteria(self, create_laptop, create_criteria, create_category):
        statement = ''' 
        INSERT INTO discrete_criteria(laptop,criteria,category)
        VALUES (?,?,?)
        '''

        result = self.cursor.execute(statement, (create_laptop, create_criteria, create_category))
        result = self.connection.commit()
        return result
    
    def get_discrete_criteria(self, selected_discrete_criteria):
        statement = '''
        SELECT * FROM discrete_criteria where laptop = '{}'
        '''.format(selected_discrete_criteria)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def update_discrete_criteria(self, update_laptop, update_criteria, update_category,
                            current_laptop, current_criteria, current_category):
        statement = '''
        update discrete_criteria set laptop=?, criteria=?, category=?
                        where laptop=? and criteria=? and category=?
        '''

        result = self.cursor.execute(statement, (update_laptop, update_criteria, update_category,
                                                current_laptop, current_criteria, current_category))
        result = self.connection.commit()
        return result

    def delete_discrete_criteria(self,  current_laptop, current_criteria, current_category):
        statement = '''
        delete from discrete_criteria where laptop=? and criteria=? and category=?
        '''

        result = self.cursor.execute(statement, (current_laptop, current_criteria, current_category))
        result = self.connection.commit()
        return result


    # DATA LAPTOP

    def read_laptop(self):
        statement = '''
        SELECT * from laptop
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_laptop(self, create_id, create_detailLink, create_laptopName):
        statement = ''' 
        INSERT INTO laptop(id,detailLink,LaptopName)
        VALUES (?,?,?)
        '''

        result = self.cursor.execute(statement, (create_id, create_detailLink, create_laptopName))
        result = self.connection.commit()
        return result
    
    def get_laptop(self, selected_laptop):
        statement = '''
        SELECT * FROM laptop where id= '{}'
        '''.format(selected_laptop)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def update_laptop(self, update_id, update_detailLink, update_laptopName,
                        current_id, current_detailLink, current_laptopName):
        statement = '''
        update laptop set id=?, detailLink=?, laptopName=?
                        where id=? and detailLink=? and laptopName=? 
        '''

        result = self.cursor.execute(statement, (update_id, update_detailLink, update_laptopName,
                                                current_id, current_detailLink, current_laptopName))
        result = self.connection.commit()
        return result

    def delete_laptop(self,  current_id, current_detailLink, current_laptopName):
        statement = '''
        delete from laptop where id=? and detailLink=? and laptopName=?
        '''

        result = self.cursor.execute(statement, (current_id, current_detailLink, current_laptopName))
        result = self.connection.commit()
        return result


    # DATA NUMERIC CRITERIA

    def read_numeric_criteria(self):
        statement = '''
        SELECT * from numeric_criteria
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_numeric_criteria(self, create_laptop, create_criteria, create_value):
        statement = ''' 
        INSERT INTO numeric_criteria(laptop,criteria,value)
        VALUES (?,?,?)
        '''

        result = self.cursor.execute(statement, (create_laptop, create_criteria, create_value))
        result = self.connection.commit()
        return result
    
    def get_numeric_criteria(self, selected_numeric_criteria):
        statement = '''
        SELECT * FROM numeric_criteria where laptop = '{}'
        '''.format(selected_numeric_criteria)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def update_numeric_criteria(self, update_laptop, update_criteria, update_value,
                            current_laptop, current_criteria, current_value):
        statement = '''
        update numeric_criteria set laptop=?, criteria=?, value=?
                        where laptop=? and criteria=? and value=?
        '''

        result = self.cursor.execute(statement, (update_laptop, update_criteria, update_value,
                                                current_laptop, current_criteria, current_value))
        result = self.connection.commit()
        return result

    def delete_numeric_criteria(self,  current_laptop, current_criteria, current_value):
        statement = '''
        delete from numeric_criteria where laptop=? and criteria=? and value=?
        '''

        result = self.cursor.execute(statement, (current_laptop, current_criteria, current_value))
        result = self.connection.commit()
        return result

    

    # DATA SUB CRITERIA




    def read_sub_criteria(self):
        statement = '''
        SELECT * from sub_criteria
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_sub_criteria(self, create_id, create_kelas, create_weight):
        statement = ''' 
        INSERT INTO sub_criteria(id,kelas,weight)
        VALUES (?,?,?)
        '''

        result = self.cursor.execute(statement, (create_id, create_kelas, create_weight))
        result = self.connection.commit()
        return result
    
    # def get_sub_criteria(self, selected_sub_criteria):
    #     statement = '''
    #     SELECT * FROM sub_criteria where id= '{}'
    #     '''.format(selected_sub_criteria)

    #     result = self.cursor.execute(statement)
    #     result = self.cursor.fetchall()
    #     return result

    def update_sub_criteria(self, update_id, update_kelas, update_weight,
                        current_id, current_kelas, current_weight):
        statement = '''
        update sub_criteria set id=?, kelas=?, weight=?
                        where id=? and kelas=? and weight=? 
        '''

        result = self.cursor.execute(statement, (update_id, update_kelas, update_weight,
                                                current_id, current_kelas, current_weight))
        result = self.connection.commit()
        return result

    def delete_sub_criteria(self, current_id, current_kelas, current_weight):
        statement = '''
        delete from sub_criteria where id=? and kelas=? and weight=?
        '''

        result = self.cursor.execute(statement, (current_id, current_kelas, current_weight))
        result = self.connection.commit()
        return result


    
    # DATA WEIGHT

    
    def read_weight(self):
        statement = '''
        SELECT * from weight
        ''' 

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result
    

    def create_weight(self, create_id, create_criteria, create_value, create_weight):
        statement = ''' 
        INSERT INTO weight(id,criteria,value,weight)
        VALUES (?,?,?,?)
        '''

        result = self.cursor.execute(statement, (create_id, create_criteria, create_value, create_weight))
        result = self.connection.commit()
        return result
    
    def get_weight(self, selected_weight):
        statement = '''
        SELECT * FROM weight where id = '{}'
        '''.format(selected_weight)

        result = self.cursor.execute(statement)
        result = self.cursor.fetchall()
        return result

    def update_weight(self, update_id, update_criteria, update_value, update_weight, current_id, current_criteria, current_value, current_weight):
        statement = '''
        update weight set id=?, criteria=?, value=?, weight=? where id=? and criteria=? and value=? and weight=?
        '''

        result = self.cursor.execute(statement, (update_id, update_criteria, update_value, update_weight, current_id, current_criteria,current_value, current_weight))
        result = self.connection.commit()
        return result

    def delete_weight(self, current_id, current_criteria, current_value, current_weight):
        statement = '''
        delete from weight where id=? and criteria=? and value=? and weight=?
        '''

        result = self.cursor.execute(statement, (current_id, current_criteria, current_value, current_weight))
        result = self.connection.commit()
        return result

#endregion

    def read_categorization_from_criteria(self, criteria):
        statement ='''
        SELECT ID, specification FROM categorization
        WHERE criteria=?
        '''

        result = self.cursor.execute(statement, str(criteria))
        result = self.cursor.fetchall()
        return result
    
    def create_laptop(self, laptopName, detailLink, discreteCriteria=[], numericCriteria=[]):
        statement = '''
        INSERT INTO laptop(detailLink, laptopName)
        VALUES (?,?)
        '''
        result = self.cursor.execute(statement, (detailLink, laptopName))
        result = self.connection.commit()
        newRowID = self.cursor.lastrowid

        for row in discreteCriteria:
            statement2 = '''
            INSERT INTO discrete_criteria(laptop, criteria, category)
            VALUES (?,?,?)
            '''
            result = self.cursor.execute(statement2, (str(newRowID), str(row[0]), str(row[1])))
            result = self.connection.commit()

        for row in numericCriteria:
            statement3 = '''
            INSERT INTO numeric_criteria(laptop, criteria, value)
            VALUES (?,?,?)
            '''

            result = self.cursor.execute(statement3, (str(newRowID), str(row[0]), str(row[1])))
            result = self.connection.commit()
    
    def update_laptop(self, id_laptop, detailLink, laptopName, discreteCriteria=[], numericCriteria=[]):
        statement = '''
        UPDATE laptop SET 
        detailLink = ?, laptopName = ?
        WHERE ID = ?
        '''
        result = self.cursor.execute(statement, (detailLink, laptopName, str(id_laptop)))
        result = self.connection.commit()

        for row in discreteCriteria:
            statement2 = '''
            UPDATE discrete_criteria SET
            category = ?
            WHERE laptop = ? AND criteria = ?
            '''

            result = self.cursor.execute(statement2, (str(row[1]), str(id_laptop), str(row[0])))
            result = self.connection.commit()

        for row in numericCriteria:
            statement3 = '''
            UPDATE numeric_criteria SET
            value = ?
            WHERE laptop = ? AND criteria = ?
            '''

            result = self.cursor.execute(statement3, (str(row[1]), str(id_laptop), str(row[0])))
            result = self.connection.commit()
    
    def delete_laptop(self, id_laptop):
        statement = '''
        DELETE FROM discrete_criteria WHERE laptop = ?
        '''
        result = self.cursor.execute(statement, (str(id_laptop),))
        self.connection.commit()

        statement2 = '''
        DELETE FROM numeric_criteria WHERE laptop = ?
        '''
        result = self.cursor.execute(statement2, (str(id_laptop),))
        self.connection.commit()

        statement3 = '''
        DELETE FROM laptop WHERE ID = ?
        '''
        result = self.cursor.execute(statement3, (str(id_laptop),))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

