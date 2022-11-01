from flask import Blueprint

from ..services.user import UserService


bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

@bp.route('/createUser', methods=['POST'])
def create_user():
    return UserService.create_user()

@bp.route('/login', methods=['POST'])
def login():
    return UserService.login()