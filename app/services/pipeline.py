from flask import request, current_app
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

from ..utils.BJW.core.jenkins import *
from ..utils.BJW.core.pipeline import *


load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")
JENKINS_ID = os.environ.get("JENKINS_ID")
JENKINS_PW = os.environ.get("JENKINS_PW")

class PipelineSerialize:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        print(f"PipelineSerialize Data: {self.data}")

    def check(self):
        if(
            not self.data['pipeline_name'] 
            or not self.data["branch"] 
            or not self.data["repo_url"] 
            or not self.data["tools"]):
            return False
        else:
            return True
        
    def run_param_check(self):
        if(not self.data['pipeline_name'] or not self.data["branch"]):
            return False
        else:
            return True

    def get_element(self, key):
        return self.data[key]
    
    def set_element(self, key, data):
        self.data[key] = data
        return self.data

class PipelineService:
    # 파이프라인 생성
    def create_pipeline():
        try:
            params = PipelineSerialize(request.get_json())
        except Exception as e:
            current_app.logger.debug("[create_pipeline] error")
            current_app.logger.debug(e)
            return resp(500, "create pipeline failed")

        if params.check() == False:
            return resp(400, "check your values")
            
        tool_dict = params.get_element("tools")
        tool_dict["BUILD"] = { "NodeJS": True } 
        # jenkins파일이 가지고 있는 tool 목록들 가져오기
        # if ( tools = JenKinsHasToolQuery):
        #     resp(500)
        '''
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
        '''

        # 파이프라인 생성
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
        except Exception as e:
            current_app.logger.debug("[create_pipeline] Jenkins constructor error")
            current_app.logger.debug(e)
            return resp(500, "create pipeline failed")
        
        tools = json.dumps(tool_dict)

        try:
            get_dict = dict(params.data)
            get_dict.pop('pipeline_name')
            get_dict.pop('tools')
            
            jenkins.create_pipeline(
                params.get_element("pipeline_name"),
                params.get_element("repo_url"),
                params.get_element("branch"),
                tools,
                **get_dict
            )
            
        except Exception as e:
            current_app.logger.debug("[create_pipeline] Jenkins.create_pipeline() error")
            current_app.logger.debug(e)
            return resp(500, "create pipeline failed")
        
        return resp(201, "create pipeline success")

    # 파이프라인 리스트 return (한승이 모듈 사용하기)
    def pipeline_list():
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
        except Exception as e:
            current_app.logger.debug("[pipeline_list] Jenkins constructor error")
            current_app.logger.debug(e)
            return resp(500, "get pipeline failed")
        
        try:
            result = jenkins['pipeline_list']
        except Exception as e:
            current_app.logger.debug("[create_pipeline] Jenkins['pipeline_list'] error")
            current_app.logger.debug(e)
            return resp(500, "get pipeline failed")
        
        return resp(201, "pipeline list success", result)
        

    # 파이프라인 수정(한승이 모듈 사용하기)
    # def update_pipeline():

    # 파이프라인 제거
    def delete_pipeline():
        try:
            params = PipelineSerialize(request.get_json())
        except Exception as e:
            current_app.logger.debug("[delete pipeline] error")
            current_app.logger.debug(e)
            return resp(500, "delete pipeline failed")
        
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            pipeline = jenkins.get_pipeline(params.get_element("pipeline_name"), params.get_element("branch"))
        except Exception as e:
            current_app.logger.debug("[delete pipeline] Pipeline constructor error")
            current_app.logger.debug(e)
            return resp(500, "delete pipeline failed")
        
        try:
            pipeline.delete()
        except Exception as e:
            current_app.logger.debug("[delete pipeline] Pipeline.delete() error")
            current_app.logger.debug(e)
            return resp(500, "delete pipeline failed")
        
        return resp(201, "pipeline delete success")

    # 파이프라인 실행시키기
    def run_pipeline():
        try:
            params = PipelineSerialize(request.get_json())
        except Exception as e:
            current_app.logger.debug("[run_pipeline] error")
            current_app.logger.debug(e)
            return resp(500, "run pipeline failed")

        if params.run_param_check() == False:
            return resp(400, "check your values")

        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            pipeline = jenkins.get_pipeline(params.get_element("pipeline_name"), params.get_element("branch"))
        except Exception as e:
            current_app.logger.debug("[run_pipeline] Pipeline constructor error")
            current_app.logger.debug(e)
            return resp(500, "run pipeline failed")
        
        # 파이프라인 실행
        try:
            pipeline.run()
        except Exception as e:
            current_app.logger.debug("[run_pipeline] Pipeline.run_pipeline() error")
            current_app.logger.debug(e)
            return resp(500, "run pipeline failed")
            
        return resp(200, "run pipeline success")

    def get_stream():
        try:
            params = PipelineSerialize(request.get_json())
        except Exception as e:
            current_app.logger.debug("[get_stream] Pipeline Serialize error")
            current_app.logger.debug(e)
            return resp(500, "get stream failed")

        if params.run_param_check() == False:
            return resp(400, "check your values")

        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            pipeline = jenkins.get_pipeline(params.get_element("pipeline_name"), params.get_element("branch"))
        except Exception as e:
            current_app.logger.debug("[get_stream] Pipeline constructor error")
            current_app.logger.debug(e)
            return resp(500, "get stream failed")

        try:
            import asyncio
            import websockets

            async def accept(websocket, path):
                for line in pipeline['stream']:
                    yield websocket.send(line)

            port = request.environ.get('REMOTE_PORT')
            start_server = websockets.serve(accept, "localhost", 52200)
            asyncio.get_event_loop().run_until_complete(start_server)

        except Exception as e:
            current_app.logger.debug("[get_stream] yielding stream error")
            current_app.logger.debug(e)
            return resp(500, "get stream failed")
        
    def get_jenkinsfiles():
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            result = jenkins['jenkinsfiles']

        except Exception as e:
            current_app.logger.debug("[get_jenkinsfiles] Jenkins constructor error")
            current_app.logger.debug(e)
            return resp(500, "get jenkinsfiles failed")

        return resp(201, "get jenkinsfiles success!", result)
    
    def get_status():
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            result = jenkins['jenkinsfiles']

        except Exception as e:
            current_app.logger.debug("[get_jenkinsfiles] Jenkins constructor error")
            current_app.logger.debug(e)
            return resp(500, "get jenkinsfiles failed")

        return resp(201, "get jenkinsfiles success!", result)
    
    def get_status():
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            result = jenkins.get_building()

        except Exception as e:
            current_app.logger.debug("[get_status] Jenkins constructor error")
            current_app.logger.debug(e)
            return resp(500, "get status failed")

        return resp(201, "get status success!", result)

    def get_pipeline():
        try:
            params = PipelineSerialize(request.get_json())
        except Exception as e:
            current_app.logger.debug("[get_pipeline] Pipeline Serialize error")
            current_app.logger.debug(e)
            return resp(500, "get pipeline failed")

        if params.run_param_check() == False:
            return resp(400, "check your values")
        try:
            jenkins = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            pipeline = jenkins.get_pipeline(params.get_element("pipeline_name"), params.get_element("branch"))

        except Exception as e:
            current_app.logger.debug("[get_pipeline] Jenkins constructor error")
            current_app.logger.debug(e)
            return resp(500, "get pipeline failed")

        try:
            result = pipeline['overall_data']

        except Exception as e:
            current_app.logger.debug("[get_pipeline] Pipeline['overall_data'] error")
            current_app.logger.debug(e)
            return resp(500, "get pipeline failed")

        return resp(201, "overall pipeline data success!", result)


