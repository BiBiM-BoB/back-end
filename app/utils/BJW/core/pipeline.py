import jenkinsapi
from jenkinsapi.utils.crumb_requester import CrumbRequester

from .jenkins import Jenkins
from .utils.Initializer import Initializer
from .generators.JenkinsfileGenerator import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator
from .utils.Debug_Initializer import DebugInitializer


class Pipeline:
    def __init__(self, jenkins_url, jenkins_username, jenkins_token, pipeline_name, mode=None, **kwargs):
        self.pipeline_name = pipeline_name
        self.url = jenkins_url
        self.username = jenkins_username
        self.token = jenkins_token

        if not mode:
            self.initializer = Initializer(jenkins_url)
        if mode == 'DEBUG':
            self.initializer = DebugInitializer(jenkins_url)
            self.initializer.debug_mode(
                kwargs['input_dockerfile'],
                kwargs['input_script_dir']
            )
        if mode == 'PUSH':
            self.initializer = DebugInitializer(jenkins_url)
            self.initializer.push_mode(
                kwargs['code'],
                kwargs['groovy_name'],
                kwargs['input_dockerfile'],
                kwargs['input_script_dir'],
                kwargs['stage'],
                kwargs['tool_name']
            )

        self.jenkins = Jenkins(jenkins_url, jenkins_username, jenkins_token)

    def create_pipeline(self, tool_json, target, target_branch, build_token=None, *args):
        # 1. create Jenkinsfile according to tool_json
        JG = JenkinsfileGenerator(self.initializer.jenkins_git.local, self.initializer.jenkins_git.remote, self.pipeline_name)
        jenkinsfile = JG.generate_by_json(tool_json)

        # 2. create config.xml
        XG = XMLGenerator(self.initializer.jenkins_git.local, self.initializer.jenkins_git.remote, self.pipeline_name)
        xml = XG.generate(target, target_branch, jenkinsfile)

        # 3. create pipeline with that two files
        job = self.jenkins.create_job(self.pipeline_name, xml)
    
    def create_pipeline_by_raw_groovy(self, groovy, target, target_branch, build_token=None, *args):
        JG = JenkinsfileGenerator(self.initializer.jenkins_git.local, self.initializer.jenkins_git.remote, self.pipeline_name)
        jenkinsfile = JG.generate_by_raw_groovy(groovy)

        XG = XMLGenerator(self.initializer.jenkins_git.local, self.initializer.jenkins_git.remote, self.pipeline_name)
        xml = XG.generate(target, target_branch, jenkinsfile)

        job = self.jenkins.create_job(self.pipeline_name, xml)

    def run_pipeline(self):
        crumb = CrumbRequester(username=self.username, password=self.token, baseurl=self.url)
        jenkins = jenkinsapi.jenkins.Jenkins(self.url, username=self.username, password=self.token, requester=crumb)
        jenkins.build_job(self.pipeline_name)
        print(f"[+] Successfully ran pipeline {self.pipeline_name}!")

    def delete_pipeline(self):
        job = self.jenkins.delete_job(self.pipeline_name)

    def get_pipeline(self):
        pass

    def get_pipelines(self) -> list:
        pipeline_list = []
        for job in self.jenkins.iter_jobs():
            pipeline_list.append(job.full_name)
        return pipeline_list