from flask import Blueprint, Response
from ..lib import loadCSV
from ..db.models import ApplicationsModel
import os

review = Blueprint('review', __name__)

_dirname = os.path.dirname(__file__)

@review.route('/configure/upload_csv')
def doCSV():
    with open(os.path.join(_dirname, "../lib/sample.csv"), encoding="utf-8") as data:
        loadCSV.upload_csv(data)
    return Response(status=200)

@review.route('/review')
def getApplicant():
    model = ApplicationsModel.get_applications_model()
    try:
        data = model.getLockedApplicantRow(1)
        if data is None:
            data = model.getNewLockedApplicantRow(1)
    except Exception as e:
        print("exception raised while getting locked applicant")
        print(e)
    return Response(str(data))

@review.route('/review/skip')
def skipApplicant():
    model = ApplicationsModel.get_applications_model()
    try:
        model.skipApplicant(1)
        data = model.getNewLockedApplicantRow(1)
    except Exception as e:
        print("could not skip applicant")
        print(e)
    return Response(str(data))