from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from datetime import datetime
import json
from dotenv import load_dotenv
import os

from ..models import db
from ..models.pipeline import *
from ..models.user import User
from ..models.jenkins_has_tool import JenkinsHasTool, jenkins_has_tools_schema
from ..models.tool import Tool

from ..utils.db import *
from ..utils.response import resp
from ..utils.login import login_required
from ..utils.BJW.Interface import *

load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")
JENKINS_ID = os.environ.get("JENKINS_ID")
JENKINS_PW = os.environ.get("JENKINS_PW")

bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')


@bp.route('/createPipeline', methods=['POST'])
# @login_required
def create_pipeline():
    try:
        params = request.get_json()

        if(not params['pipeline_name'] or not params['repo_url'] or not params['jenkins_id'] or not params["jenkins_token"] or not params["branch"]):
            return resp(400, "check your values")
        
        tools = JenkinsHasTool.query\
            .join(Tool, JenkinsHasTool.tool_id == Tool.id)\
            .add_columns(Tool.name, Tool.stage)\
            .filter(and_(JenkinsHasTool.jenkins_id == params['jenkins_id'], JenkinsHasTool.deleteAt == None))\
            .all()

        tools_dict = {}
        for tool in tools:
            if tool.stage in tools_dict.keys():
                tools_dict[tool.stage][tool.name] = 1
            else:
                row = { f"{tool.name}": 1 }
                tools_dict[tool.stage] = row

        tools_dict = json.dumps(tools_dict)

        pipeline = PipelineInterface(JENKINS_URL, JENKINS_ID, JENKINS_PW)
        print("clear pipelineInterface =========")
        result = pipeline.createPipeline(params['pipeline_name'], params['repo_url'], tools_dict, f"*/{params['branch']}", params["jenkins_token"])

        return resp(201, "create pipeline success")
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
# @login_required
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

@bp.route('/runPipeline', methods=['POST'])
# @login_required
def run_pipeline():
    try:
        params = request.get_json()

        if( not params['pipeline_name'] or not params['branch']):
            return resp(400, "check your values")
        

        pipeline = PipelineInterface(JENKINS_URL, JENKINS_ID, JENKINS_PW)
        
        pipeline.runPipeline(f"{params['pipeline_name']}/{params['branch']}")
        
        return resp(200, "test")
        
        
    except Exception as e:
        print(e)
        return resp(500, "run pipeline failed")