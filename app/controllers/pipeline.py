from flask import Blueprint, request, jsonify
from ..models import db
from ..models.pipeline import Pipeline

bp = Blueprint('pipeline', __name__, url_prefix='/api/v1/pipeline')

@bp.route('/createPipeline', methods=['POST'])
def create_pipeline():
    result = Pipeline('/git/repo1', '~/secu/repo1', 1)
    
    db.session.add(result)
    db.session.commit()
    return "complict"