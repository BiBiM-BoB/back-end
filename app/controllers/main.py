from flask import render_template, Blueprint
from sqlalchemy import and_


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main():
    return render_template('index.html')