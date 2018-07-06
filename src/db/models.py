from . import connection
import psycopg2.sql as sql

class ApplicationsModel:
    TableName = "applications"
    Model = {}

    @classmethod
    def setModel(cls, fieldnames, sample_data):
        for field in fieldnames:
            cls.Model[field] = str # force everything into string, deal with on client
        
        cls.Model["score"] = int
        
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS %s' % ApplicationsModel.TableName)
            cursor.execute('CREATE TABLE %s ()' % ApplicationsModel.TableName)
            
            for name, data_type in cls.Model.items():
                if data_type is str:
                    postgre_type = "TEXT"
                if data_type is int:
                    postgre_type = "SMALLINT"
                if data_type is float:
                    postgre_type = "real"
                cursor.execute('ALTER TABLE %s ADD COLUMN "%s" %s' % (cls.TableName, name, postgre_type))

            conn.commit()
        except Exception as e:
            print(e)
        finally:    
            cursor.close()
            conn.close()


    def store(self, row):
        """ does an INSERT INTO with the data in the row """
        keys = []
        values = []
        for value in row.values():
            values.append(value)
        
        values.append(0)
        query = sql.SQL("INSERT INTO {} VALUES ({})").format(
            sql.Identifier(self.TableName),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        connection.execute_query(query, values)


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