from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from ..utils.db import *
from ..models import db
from ..models.pipeline import *
from ..models.user import User
from ..utils.response import resp


bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')

@bp.route('/createPipeline', methods=['POST'])
def create_pipeline():
    try:
        params = request.get_json()
        
        if(not params['repo_url'] or not params['jenkinsfile_path'] or not params['owner_id']):
            return resp(400, "check your values")
        
        user_match = User.query.filter(and_(User.id == params['owner_id'], User.deleteAt == None)).first()
        if(user_match):
            result = Pipeline(params['repo_url'], params['jenkinsfile_path'], params['owner_id'])
            db_apply([result])
            return resp(200, "create pipeline success")
        else:
            return resp(400, "create pipeline failed")

    except Exception as e:
        print(e)
        return resp(500, "create pipeline failed")

@bp.route('/pipelineList', methods=['GET'])
def pipeline_list():
    try:
        all_pipelines = Pipeline.query.filter(Pipeline.deleteAt==None)
        result = pipelines_schema.dump(all_pipelines)

        return resp(200, "success", result)
    except Exception as e:
        print(e)
        return resp(500, "get pipeline list faild")