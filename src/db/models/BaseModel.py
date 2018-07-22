from .. import connection
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
            connection.return_connection(conn)

    @classmethod
    def createTable(cls):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('CREATE TABLE "%s" ()' % cls.TableName)
            
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
            conn.rollback()
            raise(e)
        finally:
            cursor.close()
            connection.return_connection(conn)