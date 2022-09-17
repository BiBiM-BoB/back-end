from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db

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

    def __init__(self, user_id, password, nick):
        self.user_id = user_id
        self.password = password
        self.nick = nick
        self.deleteAt = None
        self.permission = 4