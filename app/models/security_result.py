from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db

class SecurityResult(db.Model):
    __tablename__ = "security_results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pipeline_id = db.Column(db.Integer, db.ForeignKey('pipelines.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 실행시킨 사람
    resultfile_path = db.Column(db.String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    def __init__(self, pipeline_id, user_id, resultfile_path):
        self.pipeline_id = pipeline_id
        self.user_id = user_id
        self.resultfile_path = resultfile_path