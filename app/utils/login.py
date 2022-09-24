from flask import request
from datetime import datetime
import jwt
from functools import wraps
from ..utils.response import resp

def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, 'secret-key', "HS256")
        if payload['exp'] < datetime.utcnow():  # 토큰이 만료된 경우
            payload = None
    except jwt.InvalidTokenError:
        payload = None
    
    return payload

# decorator 함수
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        access_token = request.cookies.get('access_token')
        if access_token is not None:
            payload = check_access_token(access_token) # 토큰 유효성 확인
            if payload is None:
                return resp(401, "token failed")
        else: # 토큰이 없는 경우
            return resp(401, "no token")

        return f(*args, **kwagrs)

    return decorated_function