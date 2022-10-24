from flask import request
from sqlalchemy import and_, or_
from datetime import datetime
from dotenv import load_dotenv
import json
import os

from ..models.pipeline import *
from ..models.jenkins_has_tool import JenkinsHasTool
from ..models.tool import Tool

from ..utils.response import resp
from ..utils.db import db_apply
from ..utils.BJW.Interface import *


load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")
JENKINS_ID = os.environ.get("JENKINS_ID")
JENKINS_PW = os.environ.get("JENKINS_PW")

class PipelineService:
    # 파이프라인 생성
    def create_pipeline():
        try:
            params = request.get_json()

            if(not params['pipeline_name'] or not params['repo_url'] or not params['jenkins_id'] or not params["jenkins_token"] or not params["branch"]):
                return resp(400, "check your values")
            
            # jenkins파일이 가지고 있는 tool 목록들 가져오기
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

            # 파이프라인 생성
            pipeline = PipelineInterface(JENKINS_URL, JENKINS_ID, JENKINS_PW)

            # 한승이가 만드는 jenkins 모듈이 성공 여부 등의 결과를 넘겨주도록 수정
            result = pipeline.createPipeline(params['pipeline_name'], params['repo_url'], tools_dict, f"*/{params['branch']}", params["jenkins_token"])

            return resp(201, "create pipeline success")
        except Exception as e:
            print(e)
            return resp(500, "create pipeline failed")

    # 파이프라인 리스트 return (한승이 모듈 사용하기)
    # def pipeline_list():

    # 파이프라인 수정(한승이 모듈 사용하기)
    # def update_pipeline():

    # 파이프라인 제거(한승이 모듈 사용하기)
    # def delete_pipeline():

    # 파이프라인 실행시키기(한승이 모듈 사용하기)
    def run_pipeline():
        try:
            params = request.get_json()

            if( not params['pipeline_name'] or not params['branch']):
                return resp(400, "check your values")        

            # jenkins 설정
            pipeline = PipelineInterface(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            
            # 파이프라인 실행(추후, return 값 받아서 handling하기)
            pipeline.runPipeline(f"{params['pipeline_name']}/{params['branch']}")
            
            return resp(200, "test")
        
        except Exception as e:
            print(e)
            return resp(500, "run pipeline failed")