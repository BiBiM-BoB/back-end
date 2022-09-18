from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db, ma

class SecurityResult(db.Model):
    __tablename__ = "security_results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pipeline_id = db.Column(db.Integer, db.ForeignKey('pipelines.id'), nullable=False)
    pipeline_name = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 실행시킨 사람
    resultfile_path = db.Column(db.String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    def __init__(self, pipeline_id, pipeline_name, user_id, resultfile_path):
        self.pipeline_id = pipeline_id
        self.pipeline_name = pipeline_name
        self.user_id = user_id
        self.resultfile_path = resultfile_path

class SecurityResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pipeline_id', 'pipeline_name', 'user_id', 'resultfile_path', 'createAt', 'updateAt', 'deleteAt')

security_result_schema = SecurityResultSchema()
security_results_schema = SecurityResultSchema(many=True)