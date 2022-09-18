from flask import Blueprint, request, jsonify
from ..models import db
from ..models.user import User
from ..utils.db import db_apply

bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

@bp.route('/createUser', methods=['POST'])
def create_user():
    try:
        params = request.get_json()
        if(not params['user_id'] or not params['password'] or not params['nick']):
            return "check your value"

        user_match = User.query.filter_by(user_id=params['user_id']).all()

        if(not user_match):
            result = User(params['user_id'], params['password'], params['nick'])
            db_apply([result])
        else:
            return "있는 유저" # 추후, 반환값 통일 후 msg: 로 넘김

    except Exception as e:
        print(e)
        return "user create faild"
    return "complict"