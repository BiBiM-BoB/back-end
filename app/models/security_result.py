from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db, ma

class SecurityResult(db.Model):
    __tablename__ = "security_results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pipeline_id = db.Column(db.Integer, db.ForeignKey('pipelines.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 실행시킨 사람
    resultfile_path = db.Column(db.String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    step = db.Column(db.String(10), nullable=False)
    high = db.Column(db.Integer)
    middle = db.Column(db.Integer)
    low = db.Column(db.Integer)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    def __init__(self, pipeline_id, user_id, resultfile_path, step, high, middle, low):
        self.pipeline_id = pipeline_id
        self.user_id = user_id
        self.resultfile_path = resultfile_path
        self.step = step
        self.high = high
        self.middle = middle
        self.low = low

class SecurityResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pipeline_id', 'user_id', 'resultfile_path', 'step', 'high', 'middle', 'low', 'createAt', 'updateAt', 'deleteAt')

security_result_schema = SecurityResultSchema()
security_results_schema = SecurityResultSchema(many=True)