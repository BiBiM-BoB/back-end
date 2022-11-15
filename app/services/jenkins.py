from flask import request
from dotenv import load_dotenv
import os

from ..models.jenkins_has_tool import JenkinsHasTool
from ..models.jenkins import Jenkins
from ..models.tool import Tool, tools_schema

from ..utils.db import db_apply
from ..utils.response import resp
# from ..utils.jenkins_util.custom_jenkins import *
from ..utils.login import *

load_dotenv()
BASE_JENKINS_PATH = os.environ.get("BASE_JENKINS_PATH")

class JenkinsService:
    def create_jenkinsfile():
        try:
            params = request.get_json()

            if(not params['name']):
                return resp(400, "check your values")

            # front 연동전 hard coding
            # tools = params['tools']
            tools = { 'sis': True, 'ZAP': True, "tt": False }
            # owner_id = who()
            owner_id = 1
            
            select_toollist = list()
            
            for i in tools:
                if(tools[i] == True):
                    select_toollist.append(i)
                elif (tools[i] == False):
                    pass
                else:
                    raise("failed values")

            # 동일한 jenkinsfile명 검색
            jenkins_match = Jenkins.query.filter(Jenkins.name == params['name']).all()
            if(not jenkins_match):
                j_result = Jenkins(params['name'], BASE_JENKINS_PATH + params['name'], "security", owner_id)
                db_apply([j_result])
            else:
                return resp(409, "create tool failed")

            # jenkins id 가져오기
            jenkins = Jenkins.query.filter(Jenkins.name == params['name']).first()
            jenkins_id = jenkins.id

            # db에 등록된 tool명 가져오기
            tools = Tool.query.filter(Tool.deleteAt == None)
            tools = tools_schema.dump(tools)
            tools_id_list = list()
            
            for i in tools:
                if i['name'] in select_toollist:
                    tools_id_list.append(i['id'])
            
            # jenkins가 가지고 있는 tool 목록 생성(최적화: db 접근량 제어하기)
            for tool_id in tools_id_list:
                jht_result = JenkinsHasTool(jenkins_id, tool_id)
                db_apply([jht_result])

            return resp(200, "success")

        except Exception as e:
            print(e)
            return resp(500, "failed")