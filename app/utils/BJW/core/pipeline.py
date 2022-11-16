from .jenkins import Jenkins
from .utils import Initializer
from .generators.JenkinsfileGenerator import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator


class Pipeline:
    def __init__(self, jenkins_url, jenkins_username, jenkins_token, pipeline_name,):
        self.initializer = Initializer()
        self.jenkins = Jenkins(jenkins_url, jenkins_username, jenkins_token)
        self.pipeline_name = pipeline_name

    def create_pipeline(self, tool_json, target, target_branch, build_token=None, *args):
        # 1. create Jenkinsfile according to tool_json
        JG = JenkinsfileGenerator(self.initializer.jenkins_git.local, self.initializer.jenkins_git.remote, self.pipeline_name)
        jenkinsfile = JG.generate_by_json(tool_json)

        # 2. create config.xml
        XG = XMLGenerator(self.initializer.jenkins_git.local, self.initializer.jenkins_git.remote, self.pipeline_name)
        xml = XG.generate(target, target_branch, jenkinsfile)

        # 3. create pipeline with that two files
        job = self.jenkins.create_job(self.pipeline_name, xml)
        

    def run_pipeline(self):
        # not sure if this function requires crumb
        job = self.jenkins.build_job(self.pipeline_name)

    def delete_pipeline(self):
        job = self.jenkins.delete_job(self.pipeline_name)

    def get_pipeline(self):
        pass

    def get_pipelines(self) -> list:
        pipeline_list = []
        for job in self.jenkins.iter_jobs():
            pipeline_list.append(job.full_name)
        return pipeline_list