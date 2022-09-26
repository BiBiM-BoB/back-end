from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from ..utils.db import *
from ..models import db
from ..models.pipeline import *
from ..models.user import User
from ..utils.response import resp
from ..utils.login import login_required


bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')

@bp.route('/createPipeline', methods=['POST'])
@login_required
def create_pipeline():
    try:
        params = request.get_json()
        
        if(not params['pipeline_name'] or not params['repo_url'] or not params['jenkinsfile_path_deploy'] or not params['jenkinsfile_path_security'] or not params['owner_id']):
            return resp(400, "check your values")

        user_match = User.query.filter(and_(User.id == params['owner_id'], User.deleteAt == None)).first()
        if(user_match):
            result = Pipeline(params['pipeline_name'], params['repo_url'], params['jenkinsfile_path_deploy'], params['jenkinsfile_path_security'], params['owner_id'])
            db_apply([result])
            return resp(201, "create pipeline success")
        else:
            return resp(400, "create pipeline failed")

    except Exception as e:
        print(e)
        return resp(500, "create pipeline failed")

@bp.route('/pipelineList', methods=['GET'])
@login_required
def pipeline_list():
    try:
        all_pipelines = Pipeline.query.filter(Pipeline.deleteAt==None)
        result = pipelines_schema.dump(all_pipelines)

        return resp(200, "success", result)
    except Exception as e:
        print(e)
        return resp(500, "get pipeline list failed")