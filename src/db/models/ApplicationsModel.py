import psycopg2.sql as sql
import psycopg2.extras as extras
import csv
import datetime
from .BaseModel import BaseModel
from .UserModel import UserModel
from .. import connection

class ApplicationsModel(BaseModel):
    TableName = "applications"
    Model = {}

    @classmethod
    def setModel(cls, fieldnames, sample_data):
        cls.Model.clear()
        for field in fieldnames:
            cls.Model[field] = str # force everything into string, deal with on client
        
        cls.Model["score"] = int
        
        cls.dropTable()
        cls.createTable()

        cls.Model['user_editing'] = int
        cls.Model['id'] = int
        cls.Model['last_modified'] = datetime.datetime

        connection.execute_query('ALTER TABLE "%s" ADD COLUMN user_editing INTEGER REFERENCES "%s"(id)' % (cls.TableName, UserModel.TableName))
        connection.execute_query('ALTER TABLE "%s" ADD COLUMN id SERIAL PRIMARY KEY' % cls.TableName)
        connection.execute_query('ALTER TABLE "%s" ADD COLUMN last_modified timestamp' % cls.TableName)

        update_trigger = ("CREATE TRIGGER applicant_updated \
        BEFORE UPDATE \
        ON public.%s \
        FOR EACH ROW \
        EXECUTE PROCEDURE public.update_modified_column();" % ApplicationsModel.TableName)

        connection.execute_query(update_trigger)

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

    def getLockedApplicantRow(self, user):
        columns_to_return = list(ApplicationsModel.Model.keys())
        columns_to_return.remove('user_editing')

        query = sql.SQL("""SELECT {} FROM {} WHERE "user_editing"={} AND now() - last_modified < interval '2 hours'""").format(
            sql.SQL(', ').join([sql.Identifier(column) for column in columns_to_return]),
            sql.Identifier(ApplicationsModel.TableName),
            sql.Placeholder()
        )

        cursor = connection.execute_query(query, (user, ))
        results = cursor.fetchone()
        return results
    
    def getNewLockedApplicantRow(self, user):
        columns_to_return = list(ApplicationsModel.Model.keys())
        columns_to_return.remove('user_editing')

        conn = connection.get_connection()

        query = sql.SQL("""SELECT {} FROM {} TABLESAMPLE SYSTEM (20) WHERE "score"=0 AND ("user_editing" is null  OR now() - "last_modified" > interval '2 hours') LIMIT 1 FOR UPDATE""").format(
            sql.SQL(', ').join([sql.Identifier(column) for column in columns_to_return]),
            sql.Identifier(ApplicationsModel.TableName)
        )

        cursor = conn.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(query)

        row = cursor.fetchone()
        applicant_id = row['id']

        update_query = sql.SQL('UPDATE {} SET "user_editing"={} WHERE "id"={}').format(
            sql.Identifier(ApplicationsModel.TableName),
            sql.Placeholder(),
            sql.Placeholder()
        )
        cursor.execute(update_query, (user, applicant_id))

        conn.commit()
        connection.return_connection(conn)
        return row

    def scoreApplicant(self, id, user, score):
        query = sql.SQL("UPDATE {} SET 'score'={}, 'user_editing'=NULL WHERE 'id'={} AND 'user_editing'={}").format(
            sql.Identifier(ApplicationsModel.TableName),
            sql.Placeholder(),
            sql.Placeholder(),
            sql.Placeholder()
        )

        connection.execute_query(query, (score, id, user))
        
    def skipApplicant(self, user):
        query = sql.SQL("UPDATE {} SET 'user_editing'=NULL WHERE user_editing'={}").format(
            sql.Identifier(ApplicationsModel.TableName),
            sql.Placeholder()
        )
        connection.execute_query(query, (user, ))


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

def initialize_applications_model():
    print("checking for applications table")

    update_modified_function = sql.SQL("CREATE OR REPLACE FUNCTION public.update_modified_column() \
    RETURNS trigger \
    LANGUAGE 'plpgsql' \
    VOLATILE \
    COST 100 \
    AS $BODY$BEGIN \
    NEW.last_modified = now(); \
    RETURN NEW; \
    END; \
    $BODY$;")

    connection.execute_query(update_modified_function)

    query = sql.SQL("SELECT * \
                    FROM information_schema.columns WHERE table_name={}").format(
                        sql.Literal(ApplicationsModel.TableName)
                    )

    results = connection.execute_query(query)

    for row in results:
        data_type = row[7]
        if data_type is "text":
            data_type = str
        elif data_type is "smallint or integer":
            data_type = int

        ApplicationsModel.Model[row[3]] = data_type

    results.close()
