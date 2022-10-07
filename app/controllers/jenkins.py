from flask import Blueprint, request

from ..models.jenkins_has_tool import JenkinsHasTool
from ..models.jenkins import Jenkins
from ..models.tool import Tool, tools_schema

from ..utils.db import db_apply
from ..utils.response import resp
import requests
from ..utils.jenkins_util.custom_jenkins import *
from ..utils.login import *
import json

bp = Blueprint('jenkins', __name__, url_prefix='/api/v1/jenkins')

@bp.route('/createJenkinsFile', methods=["POST"])
# @login_required
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

        # jenkinsfile 생성 과정 진행
        # 추후 환경변수로 사용
        base_jenkins_path = '/home/bibim/my-jenkinsdir/'

        # 동일한 jenkinsfile명 검색
        jenkins_match = Jenkins.query.filter(Jenkins.name == params['name']).all()
        if(not jenkins_match):
            j_result = Jenkins(params['name'], base_jenkins_path + params['name'], "security", owner_id)
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
        

@bp.route('/signupPipeline/<id>', methods=['GET'])
# @login_required
def signupPipeline(id):
    try:
        crumb = requests.get('http://test:11edef81d279d390e2d875dc8ad32292e8@112.167.178.26:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
        url = "http://test:11edef81d279d390e2d875dc8ad32292e8@112.167.178.26:8080/job/building-a-multibranch-pipeline-project/job/master/build"
        test1, test2 = crumb.text.split(':')
        requests.post(url, headers={test1:test2})
        
        return resp(200, "success")

    except Exception as e:
        print(e)
        return resp(500, "failed")

@bp.route('/startPipeline', methods=['POST'])
# @login_required
def start_pipeline():
    try:
        call_generator(['ZAP'], 'test')
        return resp(200, "success")
    except Exception as e:
        print(e)
        return resp(500, "failed")