from flask import Blueprint, request

from ..services.jenkins import JenkinsService


bp = Blueprint('jenkins', __name__, url_prefix='/api/v1/jenkins')

@bp.route('/createJenkinsFile', methods=["POST"])
# @login_required
def create_jenkinsfile():
    return JenkinsService.create_jenkinsfile()