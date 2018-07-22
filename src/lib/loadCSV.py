from ..db.models import ApplicationsModel
from random import shuffle
import csv

def upload_csv(csv_file):
    """
    Read a csv row by row to store into the database 
    use the header to initialize the database

    csvFile -- file opened by the controller
    """

    reader = csv.DictReader(csv_file)

    ApplicationsModel.set_applications_model(reader) # reset the database

    csv_file.seek(0) # reset to first row
    next(reader) # skip the header

    applications_entry = ApplicationsModel.get_applications_model()

    rows = [row for row in reader]
    shuffle(rows)
    
    for row in rows:
        applications_entry.store(row)
