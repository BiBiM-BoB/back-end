from flask import Blueprint, request
from ..utils.db import db_apply
from ..utils.response import resp
import requests

bp = Blueprint('jenkins', __name__, url_prefix='/api/v1/jenkins/')

@bp.route('/startPipeline/<id>', ['GET'])
def start_pipeline(id):
    try:
        crumb = requests.get('http://test:11edef81d279d390e2d875dc8ad32292e8@112.167.178.26:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
        url = "http://test:11edef81d279d390e2d875dc8ad32292e8@112.167.178.26:8080/job/building-a-multibranch-pipeline-project/job/master/build"
        response = requests.post(url, headers=crumb)
        print(response)
    except Exception as e:
        print(e)
        return resp(500, "failed")
