from flask import abort, Blueprint, send_from_directory
from flask_login import login_required
import os

static_files = Blueprint('static_files', __name__)

static_path = os.path.join('applications-frontend', 'dist')  # get directory of static path


@static_files.route(
    '/', methods=['GET'],
    defaults={'path':
              'index.html'})  # redirect initial homepage requests to static files controller
# return any requested static files
@static_files.route('/<path:path>', methods=['GET'])
@login_required
def static_file(path):
    full_path = os.path.join(static_path, path)
    if not os.path.exists(full_path):
        # path not found, exit with 404
        abort(404)

    return send_from_directory(static_path, path)
