"""
Back-end nodejs/nestjs와의 통신을 위한 interface 입니다.
"""
import sys

import core.pipeline
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

from core.init import auto_init


def sendStream(stream, string):
    print(string + "\n")
    if stream == "stderr":
        sys.stderr.flush()
    elif stream == "stdout":
        sys.stdout.flush()


def getJenkinsInstance(url, username, password):
    crumb = CrumbRequester(username=username, password=password, baseurl=url)
    server = Jenkins(url, username=username, password=password, requester=crumb)
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
        self.jenkins = getJenkinsInstance(url, username, password)

    def runPipeline(self, *args):
        try:
            result = core.pipeline.run_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")


    def createPipeline(self, *args):
        # *args : pipeline_name, git_path, tool_json, branch, build_token
        result = core.pipeline.create_pipeline(self.jenkins, *args)
        sendStream("stdout", result)

    def deletePipeline(self, *args):
        try:
            result = core.pipeline.delete_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")

    def modifyPipeline(self, *args):
        try:
            result = core.pipeline.modify_pipeline(self.jenkins, *args)
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
    test = PipelineInterface("http://localhost:8080", 'test', 'test')
    test.createPipeline('testnme', "https://github.com/digininja/DVWA", json_obj, "*/master", 'tokensample')
    print("DEBUGGING..")




    """
    if len(sys.argv) < 2:
        sendStream("stderr", "ERROR: No arguments!")
    else:
        interface = PipelineInterface()

    PipelineInterface.func = getattr(PipelineInterface, sys.argv[1])
    PipelineInterface.func(*sys.argv[2:])
    """
