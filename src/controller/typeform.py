from flask import abort, Blueprint, Response, stream_with_context
from flask_login import login_required
import requests

from src.config.config import Config

typeform = Blueprint('typeform', __name__)


@typeform.route('/api/typeform/<path:download_url>/download', methods=['GET'])
@login_required
def download_typeform_file(download_url):
    headers = {'Authorization': 'Bearer {}'.format(Config.TYPEFORM_TOKEN)}
    req = requests.get(download_url, headers=headers, stream=True)

    return Response(stream_with_context(req.iter_content(chunk_size=1024)),
                    content_type=req.headers["content-type"])
