from flask import Blueprint, request, jsonify
from ..models import db
from ..models.user import User
import hashlib

bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

def password_hash(password):
    salt = "bibimbob" # 추후 env 설정 필요
    hashed = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
    return hashed

@bp.route('/createUser', methods=['POST'])
def create_user():
    params = request.get_json()
    result = User(params['user_id'], password_hash(params['password']), params['nick'])

    db.session.add(result)
    db.session.commit()
    return "complict"