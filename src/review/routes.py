from flask import Blueprint, Response
from ..lib import loadCSV
import os
review_blueprint = Blueprint('review', __name__)
_dirname = os.path.dirname(__file__)

@review_blueprint.route('/configure/upload_csv')
def doCSV():
    with open(os.path.join(_dirname, "../lib/sample.csv"), encoding="utf-8") as data:
        loadCSV.upload_csv(data)
    return Response(status=200)