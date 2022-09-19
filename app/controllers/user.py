from cgi import parse_multipart
from flask import Blueprint, request, jsonify
from ..models import db
from ..models.user import User
from ..utils.db import db_apply
from ..utils.response import resp

bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

@bp.route('/createUser', methods=['POST'])
def create_user():
    try:
        params = request.get_json()
        if(not params['user_id'] or not params['password'] or not params['nick']):
            return resp(400, "check your values")

        user_match = User.query.filter_by(user_id=params['user_id']).all()

        if(not user_match): # 유저가 없는 경우
            result = User(params['user_id'], params['password'], params['nick'])
            db_apply([result])
            return resp(200, "create user success")
        else:
            return resp(500, "user ID already exists")

    except Exception as e:
        print(e)
        return resp(500, "user create failed")