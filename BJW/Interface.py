"""
Back-end nodejs/nestjs와의 통신을 위한 interface 입니다.
"""
import sys
import core
from jenkinsapi.jenkins import Jenkins


def sendStream(stream, string):
    print(string + "\n")
    if stream == "stderr":
        sys.stderr.flush()
    elif stream == "stdout":
        sys.stdout.flush()


def getJenkinsInstance(url, username, password):
    # TODO
    server = Jenkins(url, username=username, password=password)
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
        self.jenkins = getJenkinsInstance(url, username, password)

    def runPipeline(self, *args):
        try:
            result = core.run_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")


    def createPipeline(self, *args):
        try:
            result = core.create_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")

    def deletePipeline(self, *args):
        try:
            result = core.delete_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")

    def modifyPipeline(self, *args):
        try:
            result = core.modify_pipeline(self.jenkins, *args)
            sendStream("stdout", result)
        except:
            sendStream("stdout", "ERROR")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        sendStream("stderr", "ERROR: No arguments!")
    else:
        interface = PipelineInterface()

    PipelineInterface.func = getattr(PipelineInterface, sys.argv[1])
    PipelineInterface.func(*sys.argv[2:])
