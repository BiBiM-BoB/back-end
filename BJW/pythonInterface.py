import core
from jenkinsapi.jenkins import Jenkins


def getJenkinsInstance(url, id, pw):
    return Jenkins(url, id, pw)


def createPipeline(url, id, pw, *args):
    jenkins = getJenkinsInstance(url, id, pw)
    result = core.create_pipeline(jenkins, *args)
    return result
