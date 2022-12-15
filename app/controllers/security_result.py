from flask import Blueprint

from ..services.security_result import SecurityResultService

bp = Blueprint('security_result', __name__, url_prefix='/api/v1/security_result')

@bp.route('/getSecurityResult/<id>', methods=['GET'])
# @login_required
def get_security_result(id):
    return SecurityResultService.find(id)

@bp.route("/securityResultList", methods=['GET'])            
def security_result_list():
    return SecurityResultService.all_list()

@bp.route("/projectTotalSecurityResult/<id>", methods=["GET"])
def project_total_security_result(id):
    return SecurityResultService.project_id_total_aggregate(id)

@bp.route("/allPipelineTotalSecurityResult", methods=['GET'])
def all_pipeline_total_security_result():
    return SecurityResultService.all_pipeline_total_aggregate()

@bp.route("/pipelineNameTotalSecurityResult/<name>", methods=['GET'])
def pipline_name_total_security_result(name):
    return SecurityResultService.pipeline_name_total_aggregate(name)


### bibim api


@bp.route("/bibimResultList", methods=["GET"])
def bibim_result_list():
    return SecurityResultService.bibim_result_all_list()

@bp.route("/dashboardStageIssueCount", methods=["GET"])
def dashboard_stage_issue_count():
    return SecurityResultService.stage_issue_count()

# 특정 프로젝트 선택
# 특정 프로젝트의 issue stage별 카운트
@bp.route("/projectStageIssueCount/<name>", methods=["GET"])
def project_stage_issue_count(name):
    return SecurityResultService.project_stage_issue_count(name)

