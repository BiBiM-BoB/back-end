from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_
import jwt
from datetime import datetime, timedelta

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
            return resp(201, "create user success")
        else:
            return resp(409, "user ID already exists")

    except Exception as e:
        print(e)
        return resp(500, "user create failed")

@bp.route('/login', methods=['POST'])
def login():
    try:
        params = request.get_json()
        
        if(not params['user_id'] or not params['password']):
            return resp(400, "check your values")

        user_match = User.query.filter(and_(
            User.user_id==params['user_id'], 
            User.password==params['password']))
        
        if(user_match):
            payload = {
                "user_id": params['user_id'],
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
            }
            print(payload)
            token = jwt.encode(payload, "secret-key", algorithm='HS256') # 추후, 환경변수로 변경
            print("token+++++")
            print(token)
            return resp(200, "login success", { "access_token" : token })
        else:
            return resp(400, "login failed")
    except:
        return resp(500, "login failed")