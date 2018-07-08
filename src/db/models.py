from . import connection
import psycopg2.sql as sql
import csv

class ApplicationsModel:
    TableName = "applications"
    Model = {}

    @classmethod
    def setModel(cls, fieldnames, sample_data): # use sample_data later for type inference
        for field in fieldnames:
            cls.Model[field] = str # force everything into string, deal with on client
        
        cls.Model["score"] = int
        
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS "%s"' % ApplicationsModel.TableName)
            cursor.execute('CREATE TABLE "%s" ()' % ApplicationsModel.TableName)
            
            for name, data_type in cls.Model.items():
                if data_type is int:
                    postgre_type = "SMALLINT"
                elif data_type is float:
                    postgre_type = "real"
                else:
                    postgre_type = "TEXT"
                cursor.execute('ALTER TABLE "%s" ADD COLUMN "%s" %s' % (cls.TableName, name, postgre_type))

            conn.commit()
        except Exception as e:
            print(e)
        finally:    
            cursor.close()
            conn.close()
            connection.return_connection(conn)


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
    
    reader -- instance of csv.DictReader from which to get the field names and a row of data
    """
    if not isinstance(reader, csv.DictReader):
        raise TypeError("reader is not a Dict Reader")

    row = next(reader)
    ApplicationsModel.setModel(reader.fieldnames, row)

def get_applications_model():
    """just returns an instance of ApplicationsModel"""
    return ApplicationsModel()