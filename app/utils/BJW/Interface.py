import sys

from .core import pipeline
from api4jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
import jenkinsapi.jenkins

from .core.utils.Initializer import auto_init


class PipelineInterface:
    def __init__(self, url, username, password):
        auto_init(url)
        self.url = url
        self.username = username
        self.password = password
        self.jenkins = getJenkinsInstance(url, username, password)

    def runPipeline(self, pipeline_name: str, verbose=False):
        crumb = CrumbRequester(username=self.username, password=self.password, baseurl=self.url)
        jenkins = jenkinsapi.jenkins.Jenkins(self.url, username=self.username, password=self.password, requester=crumb)
        jenkins.build_job(pipeline_name)
        print(f"[+] Successfully ran pipeline {pipeline_name}!")


    def createPipeline(self, *args):
        # *args : pipeline_name, git_path, tool_json, branch, build_token
        try:
            result = pipeline.create_pipeline(self.jenkins, *args)
        except Exception as e:
            sendStream("stdout", e)

    def deletePipeline(self, *args):
        # *args : pipeline_name
        # Deletes given pipeline
        result = pipeline.delete_pipeline(self.jenkins, *args)
        sendStream("stdout", result)
        return result

    def modifyPipeline(self, *args):
        # TODO: 기능이 덜 구현
        try:
            result = pipeline.modify_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")

    def getPipelines(self, *args):
        # No argument is needed
        # returns list of all pipelines
        # ex: ['pipeline1', 'pipe2', ...]

        try:
            result = pipeline.get_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
            return result
        except Exception as e:
            sendStream("stdout", e)



if __name__ == "__main__":
    test = PipelineInterface("http://127.0.0.1:8080", 'test', 'test')
    test.deletePipeline('nodetest')
    test.getPipelines()
