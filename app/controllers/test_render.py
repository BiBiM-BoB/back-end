from flask import render_template, Blueprint

bp = Blueprint('test_render', __name__, url_prefix='/')

@bp.route('/')
def main():
    return render_template('createPipeline.html')
