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

# @bp.route('/pipelineList', methods=['GET'])

# @bp.route('/updatePipeline/<id>', methods=['POST'])

# @bp.route('/deletePipeline/<id>', methods=['POST'])

@bp.route('/runPipeline', methods=['POST'])
# @login_required
def run_pipeline():
    return PipelineService.run_pipeline()