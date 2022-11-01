from flask import Blueprint

from ..services.security_result import SecurityResultService

bp = Blueprint('security_result', __name__, url_prefix='/api/v1/security_result')

@bp.route('/getSecurityResult/<id>', methods=['GET'])
# @login_required
def get_security_result(id):
    return SecurityResultService.find(id)

@bp.route("/securityResultList", methods=['GET'])
def security_result_list():
    return SecurityResultService.all_list()
