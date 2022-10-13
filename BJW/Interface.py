"""
Back-end nodejs/nestjs와의 통신을 위한 interface 입니다.
"""
import sys

from .core import pipeline
from api4jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
import jenkinsapi.jenkins

from .core.init import auto_init


def sendStream(stream, string):
    print(string + "\n")
    if stream == "stderr":
        sys.stderr.flush()
    elif stream == "stdout":
        sys.stdout.flush()


def getJenkinsInstance(url, username, password):
    server = Jenkins(url, auth=(username, password))
    print("[+] Successfully connencted to Jenkins Server!")
    return server

class JenkinsInterface:
    def __init__(self, url, username, password):
        self.jenkins = getJenkinsInstance(url, username, password)

    def generateApiToken(self):
        try:
            result = self.jenkins.generate_new_api_token()
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")




# TODO sendStream -> stderr
class PipelineInterface:
    def __init__(self, url, username, password):
        auto_init()
        self.url = url
        self.username = username
        self.password = password
        self.jenkins = getJenkinsInstance(url, username, password)

    def runPipeline(self, pipeline_name: str):
        crumb = CrumbRequester(username=self.username, password=self.password, baseurl=self.url)
        jenkins = jenkinsapi.jenkins.Jenkins(self.url, username=self.username, password=self.password, requester=crumb)
        jenkins.build_job(pipeline_name)
        print(f"[+] Successfully ran pipeline {pipeline_name}!")


    def createPipeline(self, *args):
        try:
            # *args : pipeline_name, git_path, tool_json, branch, build_token
            result = pipeline.create_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")

    def deletePipeline(self, *args):
        try:
            result = pipeline.delete_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")

    def modifyPipeline(self, *args):
        try:
            result = pipeline.modify_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")



if __name__ == "__main__":
    import json
    json_obj = {
        'DAST': {
            'ZAP': 1
        },
        'SAST': {
            'CodeQL': 1
        },
        'SCA': {
            'DependencyCheck': 0
        },
        'SIS': {
            'GGShield': 0,
            'GitLeaks': 0
        }
    }
    json_obj = json.dumps(json_obj)
    test = PipelineInterface("http://127.0.0.1:8080", 'test', 'test')
    #test.createPipeline('nodtest', "https://github.com/contentful/the-example-app.nodejs", json_obj, "*/master", 'tokensample')
    test.runPipeline('nodetest/master')
    print("DEBUGGING..")




    """
    if len(sys.argv) < 2:
        sendStream("stderr", "ERROR: No arguments!")
    else:
        interface = PipelineInterface()

    PipelineInterface.func = getattr(PipelineInterface, sys.argv[1])
    PipelineInterface.func(*sys.argv[2:])
    """
