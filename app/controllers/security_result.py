from flask import Blueprint, request, jsonify

from ..utils.db import db_apply
from ..models import db
from ..models.security_result import *

bp = Blueprint('security_result', __name__, url_prefix='/api/v1/security_result')

@bp.route('/createSecurityResult', methods=['POST'])
def create_security_result():
    try:
        params = request.get_json()
        if(not params['pipeline_id'] or not params['pipeline_name'] or not params['user_id'] or not params['resultfile_path']):
            return "check your values"

        result = SecurityResult(params['pipeline_id'], params['pipeline_name'], params['user_id'], params['resultfile_path'])
        db_apply([result])
        
        return "complict"
    except Exception as e:
        print(e)
        return "create security result faild"