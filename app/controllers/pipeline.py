from flask import Blueprint
from dotenv import load_dotenv
import os

from ..services.pipeline import PipelineService

load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")
JENKINS_ID = os.environ.get("JENKINS_ID")
JENKINS_PW = os.environ.get("JENKINS_PW")

bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')

@bp.route('/createPipeline', methods=['POST'])
# @login_required
def create_pipeline():
    return PipelineService.create_pipeline()

@bp.route('/pipelineList', methods=['GET'])
def get_pipeline_list():
    return PipelineService.pipeline_list()

@bp.route('/getPipeline', methods=['POST'])
def get_pipeline():
    return PipelineService.get_pipeline()

@bp.route('/getJenkinsfiles', methods=['GET'])
def get_jenkinsfiles():
    return PipelineService.get_jenkinsfiles()

@bp.route('/getStatus', methods=['GET'])
def get_status():
    return PipelineService.get_status()
    
# @bp.route('/updatePipeline/<id>', methods=['POST'])

@bp.route('/deletePipeline', methods=['POST'])
def delete_pipeline():
    return PipelineService.delete_pipeline()

@bp.route('/runPipeline', methods=['POST'])
# @login_required
def run_pipeline():
    return PipelineService.run_pipeline()

@bp.route('/getStream', methods=['POST'])
def get_stream():
    return PipelineService.get_stream()
