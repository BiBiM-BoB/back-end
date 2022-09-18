from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db, ma

class Pipeline(db.Model):
    __tablename__ = "pipelines"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    repo_url = db.Column(db.String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    jenkinsfile_path = db.Column(db.String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    # relationship
    security_result = relationship('SecurityResult')
    
    def __init__(self, repo_url, jenkinsfile_path, owner_id):
        self.repo_url = repo_url
        self.jenkinsfile_path = jenkinsfile_path
        self.owner_id = owner_id

class PipelineSchema(ma.Schema):
    class Meta:
        fields = ('id', 'repo_url', 'jenkinsfile_path', 'owner_id', 'createAt', 'updateAt', 'deleteAt')

pipeline_schema = PipelineSchema()
pipelines_schema = PipelineSchema(many=True)