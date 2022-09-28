from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from ..utils.db import *
from ..models import db
from ..models.pipeline import *
from ..models.user import User
from ..utils.response import resp
from ..utils.login import login_required
from datetime import datetime


bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')

@bp.route('/createPipeline', methods=['POST'])
# @login_required
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
# @login_required
def pipeline_list():
    try:
        all_pipelines = Pipeline.query.filter(Pipeline.deleteAt==None)
        result = pipelines_schema.dump(all_pipelines)

        return resp(200, "success", result)
    except Exception as e:
        print(e)
        return resp(500, "get pipeline list failed")

@bp.route('/updatePipeline/<id>', methods=['POST'])
# @login_required
def update_pipeline(id):
    try:
        params = request.get_json()
        
        if( not params['pipeline_name'] or not params['repo_url'] or not params['jenkinsfile_path_deploy'] or not params['jenkinsfile_path_security'] or not params['owner_id']):
            return resp(400, "check your values")

        pipeline = Pipeline.query.get(id)

        if(pipeline is not None):
            pipeline.pipeline_name = params['pipeline_name']
            pipeline.repo_url = params['repo_url']
            pipeline.jenkinsfile_path_deploy = params['jenkinsfile_path_deploy']
            pipeline.jenkinsfile_path_deploy = params['jenkinsfile_path_security']
            pipeline.owner_id = params['owner_id']
            pipeline.updateAt = datetime.utcnow()
            db_apply([pipeline])

            return resp(200, "update success")
        else:
            return resp(400, "update failed")

    except Exception as e:
        print(e)
        return resp(500, "update pipeline failed")

@bp.route('/deletePipeline/<id>', methods=['POST'])
def delete_pipeline(id):
    try:
        # 권한체크
        
        # 삭제(deleteAt 추가)
        pipeline = Pipeline.query.get(id)
        
        if(pipeline is not None):
            pipeline.deleteAt = datetime.utcnow()
            db_apply([pipeline])

            return resp(200, "delete success")
        else:
            return resp(400, "delete failed")
    except Exception as e:
        print(e)
        return resp(500, "delete pipeline failed")