from . import connection
import psycopg2.sql as sql
import abc

class BaseModel(abc.ABC):
    TableName = ""
    Model = {}

    @classmethod
    def dropTable(cls):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS "%s"' % cls.TableName)
            conn.commit()
        except Exception as e:
            raise(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def createTable(cls):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('CREATE TABLE "%s" ()' % cls.TableName)
            
            for name, data_type in cls.Model.items():
                if type(data_type) is str:
                    postgre_type = data_type
                if data_type is str:
                    postgre_type = "TEXT"
                if data_type is int:
                    postgre_type = "SMALLINT"
                if data_type is float:
                    postgre_type = "real"
                cursor.execute('ALTER TABLE "%s" ADD COLUMN "%s" %s' % (cls.TableName, name, postgre_type))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise(e)
        finally:
            cursor.close()
            conn.close()


class UserModel(BaseModel):
    TableName = "user"
    Model = {}

    @classmethod
    def createUserTable(cls):
        cls.Model['id'] = int
        cls.dropTable()
        cls.createTable()
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('ALTER TABLE "%s" DROP COLUMN IF EXISTS id' % cls.TableName)
            cursor.execute('ALTER TABLE "%s" ADD COLUMN id SERIAL PRIMARY KEY' % cls.TableName)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise(e)
        finally:
            cursor.close()
            conn.close()

class ApplicationsModel(BaseModel):
    TableName = "applications"
    Model = {}

    @classmethod
    def setModel(cls, fieldnames, sample_data):
        for field in fieldnames:
            cls.Model[field] = str # force everything into string, deal with on client
        
        cls.Model["score"] = int
        
        cls.dropTable()
        cls.createTable()

        cls.Model['user_editing'] = int

        connection.execute_query('ALTER TABLE "%s" ADD COLUMN user_editing INTEGER REFERENCES "%s"(id)' % (cls.TableName, UserModel.TableName))

    def store(self, row):
        """ does an INSERT INTO with the data in the row """
        keys = []
        values = []
        for value in row.values():
            values.append(value)
        
        values.append(0) # score
        values.append(None) # user_editing

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

def get_user_model():
    return UserModel()

def initialize_user_model():
    print("checking for user table")
    results = connection.execute_query("SELECT EXISTS ( SELECT 1 FROM pg_tables WHERE tablename = 'user')")
    row = results.fetchone()
    results.close()
    print(row)
    if row[0] == False: # table has not been created
        print("initializing the user table")
        try:
            UserModel.createUserTable()
        except Exception as e:
            print(e)
