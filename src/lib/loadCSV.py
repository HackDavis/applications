from ..db import models
import csv

def _store_csv_row(row):
    """ 
    Read a line from the CSV and store it in the database using the model 

    row -- a python dictionary defining the data in the row
    """
    applications_entry = models.get_applications_model()
    applications_entry.store(row)

def upload_csv(csv_file):
    """
    Read a csv row by row to store into the database 
    use the header to initialize the database

    csvFile -- file opened by the controller
    """
    reader = csv.DictReader(csv_file)

    models.set_applications_model(reader) # reset the database

    reader = csv.DictReader(csv_file) # reset reader
    
    for row in reader:
        _store_csv_row(row)
