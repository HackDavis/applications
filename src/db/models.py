from . import connection

class ApplicationsModel:

    def __init__(self, db):
        """ store a database connection """
        self._db = db

    def store(self, row):
        """ does an INSERT INTO with the data in the row """
        pass


def setApplicationsModel(fieldNames):
    """
    sets up a global table for applications
    
    fieldNames -- a list of strings for the fields in the typeform CSV
    """
    pass

def getApplicationsModel():
    """just returns an instance of ApplicationsModel"""
    return None