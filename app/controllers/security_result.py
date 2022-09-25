from flask import Blueprint, request, jsonify

from ..utils.login import login_required

from ..utils.db import db_apply
from ..models import db
from ..models.security_result import *
from ..utils.response import resp

bp = Blueprint('security_result', __name__, url_prefix='/api/v1/security_result')

@bp.route('/createSecurityResult', methods=['POST'])
@login_required
def create_security_result():
    try:
        params = request.get_json()
        if(not params['pipeline_id'] or not params['user_id'] or not params['resultfile_path']):
            return resp(400, "check your values")

        result = SecurityResult(params['pipeline_id'], params['user_id'], params['resultfile_path'])
        db_apply([result])
        
        return resp(201, "create security result success")
    except Exception as e:
        print(e)
        return resp(500, "create security result failed")

@bp.route('/securityResultList', methods=["GET"])
@login_required
def security_result_list():
    try:
        all_security_result = SecurityResult.query.filter(SecurityResult.deleteAt==None)
        result = security_results_schema.dump(all_security_result)
        
        return resp(200, "success", result)
        
    except Exception as e:
        print(e)
        return resp(500, "get security result list failed")