from ..db import models
import csv

def _storeCSVRow(row):
    """ 
    Read a line from the CSV and store it in the database using the model 

    row -- a python dictionary defining the data in the row
    """
    applicationsEntry = models.getApplicationsModel()
    applicationsEntry.store(row)

def uploadCSV(csvFile):
    """
    Read a csv row by row to store into the database 
    use the header to initialize the database

    csvFile -- file opened by the controller
    """
    reader = csv.DictReader(csvFile)

    models.setApplicationsModel(reader.fieldnames) # reset the database
    
    for row in reader:
        _storeCSVRow(row)