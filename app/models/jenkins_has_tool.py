from sqlalchemy.orm import relationship
from datetime import datetime

from ..models import db, ma
from ..models import ToolSchema, JenkinsSchema

class JenkinsHasTool(db.Model):
    __tablename__ = "jenkins_has_tools"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    jenkins_id = db.Column(db.Integer, db.ForeignKey('jenkinses.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    createAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleteAt = db.Column(db.DateTime)

    def __init__(self, jenkins_id, tool_id):
        self.jenkins_id = jenkins_id
        self.tool_id = tool_id

class JenkinsHasToolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'jenkins_id', 'tool_id', 'createAt', 'updateAt', 'deleteAt')

class NestedJenkinsHasToolSchema(ma.Schema):
    # jenkins_has_tool_data = ma.Nested(JenkinsHasToolSchema)
    # tool = ma.Nested(ToolSchema)
    test = ma.Nested(ToolSchema)
    test2 = ma.Nested(JenkinsSchema)
    class Meta:
        fields = ('id', 'jenkins_id', 'tool_id', 'createAt', 'updateAt', 'deleteAt')

jenkins_has_tool_schema = JenkinsHasToolSchema()
jenkins_has_tools_schema = JenkinsHasToolSchema(many=True)

nested_jenkins_has_tools_schema = NestedJenkinsHasToolSchema(many=True)
