from flask import Blueprint
from ..lib import loadCSV
review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/configure')
def doCSV(page):
    with open("./lib/sample.csv") as data:
        loadCSV.upload_csv(data)