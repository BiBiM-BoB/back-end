from sqlalchemy.orm import relationship
from ..models import db, ma
from datetime import datetime
from ..models.jenkins_has_tool import JenkinsHasToolSchema

class Tool(db.Model):
    __tablename__ = 'tools'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    stage = db.Column(db.String(20), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    jenkins_has_tool = relationship("JenkinsHasTool")

    def __init__(self, name, stage):
        self.name = name
        self.stage = stage


class ToolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'stage', 'createAt', 'updateAt', 'deleteAt')

tool_schema = ToolSchema()
tools_schema = ToolSchema(many=True)
        