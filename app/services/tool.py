from flask import request
from sqlalchemy import and_

from ..utils.db import db_apply
from ..utils.response import resp

from ..models.tool import Tool, tools_schema


class ToolService:
    # 운영자가 Tool을 추가했을 때, 쉽게 db에 추가하기 위한 service
    def create_tool_name():
        try:
            params = request.get_json()

            if(not params['name'] or not params['stage']):
                return resp(400, "check your values")

            # 기존에 같은 이름의 툴이 있는지 확인
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

    def tool_list():
        # 모든 tool list 제공
        try:
            # tools DB에 들어가 있는 모든 툴의 id, 이름, stage(SAST, DAST등)을 가져옴
            all_result = Tool.query.with_entities(Tool.id, Tool.name, Tool.stage).filter(Tool.deleteAt == None)
            result = tools_schema.dump(all_result)

            return resp(200, "success", result)
        except Exception as e:
            print(e)
            return resp(500, "failed")