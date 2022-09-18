from flask import Blueprint, request, jsonify
from ..models import db
from ..models.security_result import SecurityResult

bp = Blueprint('security_result', __name__, url_prefix='/api/v1/security_result')

@bp.route('/createSecurityResult', methods=['POST'])
def create_user():
    result = SecurityResult(1, 1, '~/securityfiles/hoho')

    db.session.add(result)
    db.session.commit()
    return "complict"