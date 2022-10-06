from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db, ma

class Pipeline(db.Model):
    __tablename__ = "pipelines"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pipeline_name = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    repo_url = db.Column(db.String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    jenkins_id = db.Column(db.Integer, db.ForeignKey('pipelines.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    security_result = relationship('SecurityResult')
    
    def __init__(self, pipeline_name, repo_url, jenkins_id, owner_id):
        self.pipeline_name = pipeline_name
        self.repo_url = repo_url
        self.jenkins_id = jenkins_id
        self.owner_id = owner_id

class PipelineSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pipeline_name', 'repo_url', 'jenkins_id', 'owner_id', 'createAt', 'updateAt', 'deleteAt')

pipeline_schema = PipelineSchema()
pipelines_schema = PipelineSchema(many=True)