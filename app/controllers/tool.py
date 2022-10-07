from flask import Blueprint, request
from sqlalchemy import and_

from ..utils.login import login_required
from ..utils.db import db_apply
from ..utils.response import resp

from ..models.tool import Tool, tools_schema

bp = Blueprint('tool', __name__, url_prefix='/api/v1/tool')

@bp.route('/createToolName', methods=['POST'])
# @login_required
def create_tool_name():
    try:
        params = request.get_json()

        if(not params['name'] or not params['stage']):
            return resp(400, "check your values")

        tool_match = Tool.query.filter(
            and_(Tool.name == params['name'], 
                Tool.deleteAt == None)).all()

        if(not tool_match):
            result = Tool(params['name'], params['stage'])
            db_apply([result])
            return resp(201, "create tool success")
        else:
            return resp(409, "create tool failed")

    except Exception as e:
        print(e)
        return resp(500, "failed")

@bp.route('/toolList', methods=["GET"])
# @login_required
def tool_list():
    try:
        all_result = Tool.query.filter(Tool.deleteAt == None)
        result = tools_schema.dump(all_result)

        return resp(200, "success", result)
    except Exception as e:
        print(e)
        return resp(500, "failed")