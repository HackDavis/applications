from .BaseModel import BaseModel
from .. import connection

class UserModel(BaseModel):
    TableName = "user"
    Model = {}

    @classmethod
    def createUserTable(cls):
        cls.dropTable()
        cls.createTable()
        cls.Model['id'] = int

        conn = connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('ALTER TABLE "%s" ADD COLUMN id SERIAL PRIMARY KEY' % cls.TableName)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise(e)
        finally:
            cursor.close()
            conn.close()

def get_user_model():
    return UserModel()

def initialize_user_model():
    print("checking for user table")
    results = connection.execute_query("SELECT EXISTS ( SELECT 1 FROM pg_tables WHERE tablename = 'user')")
    row = results.fetchone()
    results.close()

    if row[0] == False: # table has not been created
        print("initializing the user table")
        try:
            UserModel.createUserTable()
        except Exception as e:
            print(e)
