import psycopg2.sql as sql
import csv
from .BaseModel import BaseModel
from .UserModel import UserModel
from .. import connection

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
    
    reader -- instance of csv.DictReader from which to get the field names and a row of data
    """
    if not isinstance(reader, csv.DictReader):
        raise TypeError("reader is not a Dict Reader")

    row = next(reader)
    ApplicationsModel.setModel(reader.fieldnames, row)

def get_applications_model():
    """just returns an instance of ApplicationsModel"""
    return ApplicationsModel()

