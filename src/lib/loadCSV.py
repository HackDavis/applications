from ..db.models import ApplicationsModel
import csv


def upload_csv(csv_file):
    """
    Read a csv row by row to store into the database 
    use the header to initialize the database

    csvFile -- file opened by the controller
    """
    reader = csv.DictReader(csv_file)

    ApplicationsModel.set_applications_model(reader)  # reset the database

    csv_file.seek(0)  # reset to first row
    next(reader)  # skip the header

    applications_entry = ApplicationsModel.get_applications_model()

    for row in reader:
        applications_entry.store(row)
