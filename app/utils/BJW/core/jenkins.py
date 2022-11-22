'''OneDayGinger

# Properties
    (1) pipeline_list

# Functions
    (1) create_pipeline -> Pipeline
    (2) get_pipeline -> Pipeline
    (3) generate_new_api_token -> str
'''

import api4jenkins
from api4jenkins.job import WorkflowJob

from .pipeline import Pipeline
from .initializer.Initializer import Initializer
from .generators.JenkinsfileGenerator import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator


class PipelineExistsError(Exception):
    def __init__(self, pipeline_name, branch):
        msg = f"Pipeline {pipeline_name} / {branch} already exists!"
        super().__init__(msg)


class Jenkins(api4jenkins.Jenkins):
    def __init__(self, url, username, token):
        super().__init__(url, auth=(username, token))

    def create_pipeline(self, pipeline_name, target, target_branch, tool_json=None, groovy=None, token=None, *args) -> Pipeline:

        #  check if pipeline already exists
        check = (pipeline_name, target_branch)
        if check in self.get_pipelines(True):
            raise PipelineExistsError(pipeline_name, target_branch)

        # 0. Init gits
        initializer = Initializer(self.url)

        # 1. create Jenkinsfile according to tool_json
        JG = JenkinsfileGenerator(
            initializer.jenkins_git.local,
            initializer.jenkins_git.remote,
            pipeline_name
        )
        if tool_json:
            jenkinsfile = JG.generate_by_json(tool_json)
        if groovy:
            jenkinsfile = JG.generate_by_raw_groovy(groovy)

        # 2. create config.xml
        XG = XMLGenerator(
            initializer.jenkins_git.local,
            initializer.jenkins_git.remote,
            pipeline_name
        )
        xml = XG.generate(target, target_branch, jenkinsfile)

        # 3. create pipeline with that two files
        job = self.jenkins.create_job(self.pipeline_name, xml)

        return Pipeline(self, pipeline_name, target_branch, token)

    def get_pipeline(self, pipeline_name, branch, token=None) -> Pipeline:
        return Pipeline(self, pipeline_name, branch, token)

    @property
    def pipeline_list(self) -> list:
        return self.get_pipelines()

    def get_pipelines(self, branch=False):
        """
            Returns list of pipelines.

            if not branch:
                type: [pipeline, ...]
            else:
                type: [(pipeline, branch), (..., ...), ...]
        """
        pipeline_list = []

        if not branch:
            for job in self.iter_jobs():
                pipeline_list.append(job.name)

        if branch:
            for job in self.iter_jobs(4):
                if type(job) is WorkflowJob:
                    temp = job.full_name.split('/')
                    pipeline_list.append(tuple(temp))

        return pipeline_list

    def __getitem__(self, key):
        return getattr(self, key)
