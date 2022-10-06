from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db, ma
import hashlib

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    nick = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
    permission = db.Column(db.Integer, nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    # relationship
    pipeline = relationship("Pipeline")
    security_result = relationship("SecurityResult")
    jenkins = relationship("Jenkins")

    def __init__(self, user_id, password, nick):
        self.user_id = user_id
        self.password = self.password_hash(password)
        self.nick = nick
        self.deleteAt = None
        self.permission = 4

    def password_hash(self, password):
        salt = "bibimbob" # 추후 env 설정 필요
        hashed = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
        return hashed
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'password', 'nick', 'permission', 'createAt', 'updateAt', 'deleteAt')

user_schema = UserSchema()
users_schema = UserSchema(many=True)