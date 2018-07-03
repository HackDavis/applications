from flask import abort, Blueprint, send_from_directory
import os

routes = Blueprint('routes', __name__)

static_path = os.path.join('applications-frontend', 'dist') # get directory of static path

@routes.route('/', defaults={'path': 'index.html'}) # redirect initial homepage requests to static files controller

# return any requested static files
@routes.route('/<path:path>', methods=['GET'])
def static_file(path):
    full_path = os.path.join(static_path, path)
    if not os.path.exists(full_path):
        # path not found, exit with 404
        abort(404)

    return send_from_directory(static_path, path)

