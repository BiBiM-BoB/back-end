from flask import Blueprint

from ..services.tool import ToolService


bp = Blueprint('tool', __name__, url_prefix='/api/v1/tool')

@bp.route('/createToolName', methods=['POST'])
# @login_required
def create_tool_name():
    return ToolService.create_tool_name()

@bp.route('/toolList', methods=["GET"])
# @login_required
def tool_list():
    return ToolService.tool_list()