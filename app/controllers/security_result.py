from flask import Blueprint

bp = Blueprint('security_result', __name__, url_prefix='/api/v1/security_result')

@bp.route('/createPipeline', methods=['POST'])
# @login_required
def create_security_result():
    return "test"