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


def getJenkinsInstance():
    # TODO
    server = Jenkins("https://127.0.0.1:8080", username="admin", password="admin")
    return server


class Interface:
    def __init__(self):
        self.jenkins = getJenkinsInstance()

    def createPipeline(self, *args):
        result = core.create_pipeline(self.jenkins, *args)
        sendStream("stdout", result)

    def deletePipeline(self, *args):
        pass

    def modifyPipeline(self, *args):
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sendStream("stderr", "ERROR: No arguments!")
    else:
        interface = Interface()

    Interface.func = getattr(Interface, sys.argv[1])
    Interface.func(*sys.argv[2:])
