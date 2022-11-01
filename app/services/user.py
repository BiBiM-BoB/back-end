from flask import request, jsonify
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os

from ..models import db
from ..models.user import User
from ..utils.db import db_apply
from ..utils.response import resp

load_dotenv()
TOKEN_SECRET_KEY = os.environ.get("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = os.environ.get("TOKEN_ALGORITHM")

class UserService:
    def create_user():
        try:
            params = request.get_json()
            if(not params['user_id'] or not params['password'] or not params['nick']):
                return resp(400, "check your values")

            user_match = User.query.filter_by(user_id=params['user_id']).all()
            
            # 기존에 있는 유저인지 확인
            if(not user_match):
                result = User(params['user_id'], params['password'], params['nick'])
                db_apply([result])
                return resp(201, "create user success")
            else:
                return resp(409, "user ID already exists")

        except Exception as e:
            print(e)
            return resp(500, "user create failed")

    def login():
        try:
            params = request.get_json()
            
            if(not params['user_id'] or not params['password']):
                return resp(400, "check your values")

            user_match = User.query.filter(and_(
                User.user_id==params['user_id'], 
                User.password==params['password'])).first()
            
            # 기존에 있는 유저인지 확인후, token 부여(60 * 60 * 24 => 1일)
            if(user_match):
                payload = {
                    "user_id": params['id'],
                    "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
                }
                token = jwt.encode(payload, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM) # 추후, 환경변수로 변경

                return resp(200, "login success", { "access_token" : token })
            else:
                return resp(400, "login failed")
        except:
            return resp(500, "login failed")