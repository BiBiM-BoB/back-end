from flask import Blueprint, request, jsonify

from ..utils.db import db_apply
from ..models import db
from ..models.pipeline import Pipeline
from ..models.user import User

bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')

@bp.route('/createPipeline', methods=['POST'])
def create_pipeline():
    try:
        params = request.get_json()
        
        if(not params['repo_url'] or not params['jenkinsfile_path'] or not params['owner_id']):
            return "check your values"
        
        user_match = User.query.filter_by(user_id=params['owner_id']).first()
        if(user_match):
            result = Pipeline(params['repo_url'], params['jenkinsfile_path'], params['owner_id'])
            db_apply([result])
        else:
            return "pipe line 생성 실패"

    except Exception as e:
        print(e)
        return "create pipeline failed"
    return "complict"

@bp.route('/pipelineList', methods=['GET'])
def pipeline_list():
    try:
        result = Pipeline.query.all()
        print(result)
    except Exception as e:
        print(e)
        return "get pipeline list faild"

    return "complict"