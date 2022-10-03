from flask import Blueprint, request
from ..utils.db import db_apply
from ..utils.response import resp
import requests
from ..utils.jenkins_util.custom_jenkins import *
from ..utils.login import *
import json

bp = Blueprint('jenkins', __name__, url_prefix='/api/v1/jenkins')

@bp.route('/startPipeline/<id>', methods=['GET'])
# @login_required
def start_pipeline(id):
    try:
        crumb = requests.get('http://test:11edef81d279d390e2d875dc8ad32292e8@112.167.178.26:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
        url = "http://test:11edef81d279d390e2d875dc8ad32292e8@112.167.178.26:8080/job/building-a-multibranch-pipeline-project/job/master/build"
        print(1)
        test1, test2 = crumb.text.split(':')
        requests.post(url, headers={test1:test2})
        print(2)
        
        return resp(200, "success")

    except Exception as e:
        print(e)
        return resp(500, "failed")

@bp.route('/createJenkinsfile', methods=['POST'])
# @login_required
def create_jenkinsfile():
    try:
        print(1)
        call_generator(['ZAP'], 'test')
        print(2)
        return resp(200, "success")
    except Exception as e:
        print(e)
        return resp(500, "failed")