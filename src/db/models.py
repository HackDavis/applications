from . import connection
import ast

class ApplicationsModel:
    TableName = "applications"
    Model = {}

    @classmethod
    def setModel(cls, fieldnames, sample_data):
        for i in len(fieldnames):
            try:
                field_type = type(ast.literal_eval(sample_data[i]))
            except ValueError:
                field_type = type(str)
            cls.Model[fieldnames[i]] = field_type
        
        cls.Model["score"] = type(int)
        
        conn = connection.get_connection()
        cursor = conn.cursor()

        cursor.execute('DROP TABLE "%s"' % ApplicationsModel.TableName)
        cursor.execute('CREATE TABLE "%s"' % ApplicationsModel.TableName)
        cursor.execute('ALTER TABLE "%s' % ApplicationsModel.TableName)
        
        for name, data_type in cls.Model.items():
            if data_type is type(str):
                postgre_type = "TEXT"
            if data_type is type(int):
                postgre_type = "SMALLINT"
            if data_type is type(float):
                postgre_type = "real"
            postgre_type = data_type
            cursor.execute('ADD COLUMN "%s" %s' % (name, postgre_type))

        conn.commit()
        conn.close()


    def store(self, row):
        """ does an INSERT INTO with the data in the row """
        keys_string = ""
        values_string = ""
        for key, value in row.items():
            keys_string += key
            keys_string += ","
            values_string += value
            values_string += ","
        
        keys_string += "score"
        values_string += "0"
        query_string = 'INSERT INTO "%s" (%s) VALUES (%s)' % (self.TableName, keys_string, values_string)
        connection.execute_query(query_string)


def set_applications_model(reader):
    """
    sets up a global table for applications
    
    fieldNames -- a list of strings for the fields in the typeform CSV
    """
    row = next(reader)
    ApplicationsModel.setModel(reader.fieldnames, row)

def get_applications_model():
    """just returns an instance of ApplicationsModel"""
    return ApplicationsModel()