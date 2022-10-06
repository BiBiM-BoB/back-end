from sqlalchemy.orm import relationship
from datetime import datetime
from ..models import db, ma

class Jenkins(db.Model):
    __tablename__ = 'jenkinses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(1024, 'utf8mb4_unicode_ci'))
    jenkinsfile_path = db.Column(db.String(1024, 'utf8mb4_unicode_ci'))
    type = db.Column(db.String(100, 'utf8mb4_unicode_ci'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    pipeline = relationship("Pipeline")
    jenkins_has_tool = relationship("JenkinsHasTool")

    def __init__(self, name, jenkinsfile_path, type):
        self.name = name
        self.jenkinsfile_path = jenkinsfile_path
        self.type = type

class JenkinsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'jenkinsfile_path', 'type', 'createAt', 'updateAt', 'deleteAt')

jenkins_schema = JenkinsSchema()
jenkinses_schema = JenkinsSchema(many=True)