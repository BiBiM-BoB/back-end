from flask import render_template, Blueprint
from sqlalchemy import and_

from ..models.user import User
from ..models.tool import Tool
from ..models.jenkins import Jenkins
from ..models.pipeline import Pipeline
from ..models.security_result import SecurityResult
from ..models.jenkins_has_tool import JenkinsHasTool, JenkinsHasToolSchema, NestedJenkinsHasToolSchema, jenkins_has_tool_schema, jenkins_has_tools_schema, nested_jenkins_has_tools_schema
from ..models.tool import tool_schema, tools_schema

from ..utils.db import db_apply, join_to_json


bp = Blueprint('test_render', __name__, url_prefix='/')

@bp.route('/')
def main():
    return render_template('createPipeline.html')


@bp.route('/testdata', methods=["GET"])
def testdata():
    result_list = list()
    result_list.append(User("test1", "1234", "test1"))
    result_list.append(User("test2", "5678", "test2"))

    result_list.append(Tool("ggshield", "SIS"))
    result_list.append(Tool("Gitleaks", "SIS"))
    result_list.append(Tool("CodeQL", "SAST"))
    result_list.append(Tool("ZAP", "DAST"))
    result_list.append(Tool("dependency-check", "SCA"))
    
    result_list.append(Jenkins("python", "/home/bibim/my-jenkinsdir/python", "security", 1))
    result_list.append(Jenkins("nodejs", "/home/bibim/my-jenkinsdir/nodejs", "security", 1))
    result_list.append(Jenkins("nodejs-deploy", "/home/bibim/my-jenkinsdir/nodejs-deploy", "deploy", 2))
    
    result_list.append(Pipeline("dev-pipeline", "github.com/python-1.3.4", 1, 1))
    result_list.append(Pipeline("dev-pipeline-2", "github.com/python/check1", 1, 1))
    result_list.append(Pipeline("dev-pipeline-3", "github.com/python/check2", 1, 2))
    result_list.append(Pipeline("new-proejct-pipeline", "github.com/nodejs/deploy", 2, 2))

    result_list.append(SecurityResult(1, 1, "/results/test1", "test1", 4, 1, 2))
    result_list.append(SecurityResult(1, 1, "/results/test2", "test2", 2, 32, 12))
    result_list.append(SecurityResult(1, 1, "/results/test3", "test3", 9, 12, 32))
    result_list.append(SecurityResult(1, 1, "/results/test4", "test4", 1, 2, 3))
    result_list.append(SecurityResult(2, 2, "/results/test1", "test1", 4, 1, 2))
    
    result_list.append(JenkinsHasTool(1, 1))
    result_list.append(JenkinsHasTool(1, 3))
    result_list.append(JenkinsHasTool(1, 2))
    result_list.append(JenkinsHasTool(2, 1))
    result_list.append(JenkinsHasTool(2, 4))
    
    db_apply(result_list)
    return "success"

@bp.route("/test", methods=["GET"])
def test_get():
    test1 = JenkinsHasTool.query\
            .join(Tool, JenkinsHasTool.tool_id == Tool.id)\
            .add_columns(Tool.name, Tool.stage)\
            .filter(and_(JenkinsHasTool.jenkins_id == 1, JenkinsHasTool.deleteAt == None))

    tools = JenkinsHasTool.query\
        .join(Tool, JenkinsHasTool.tool_id == Tool.id)\
        .add_columns(Tool)\
        .filter(and_(JenkinsHasTool.jenkins_id == 1, JenkinsHasTool.deleteAt == None))\
        .all()

    print(tools)
    print(nested_jenkins_has_tools_schema.dump(tools))

    print(join_to_json(tools, "tools", jenkins_has_tool_schema, tool_schema))

    return "test success"