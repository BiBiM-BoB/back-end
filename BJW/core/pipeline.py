from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from .generators.JenkinsfileGenerator import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator


def create_pipeline(jenkins: Jenkins, pipeline_name, git_path, tool_json, branch, build_token):
    localgitdir, jenkinsfile = JenkinsfileGenerator(pipeline_name, tool_json).post_action()
    xml = XMLGenerator(pipeline_name,
                       ("remote", git_path),
                       ("url", localgitdir),
                       # TODO: jenkinsfile local git management
                       ("remoteJenkinsFile", jenkinsfile),
                       ("name", branch),
                       # ("authToken", build_token)
                       ).post_action()
    job_instance = jenkins.create_job(pipeline_name, xml.target_xml_path)

    return "createPipeline Succeed!"


def delete_pipeline(jenkins: Jenkins, pipeline_name):
    job_instance = jenkins.delete_job(pipeline_name)

    return "deletePipeline Succeed!"


def modify_pipeline(jenkins: Jenkins, pipeline_name, workspace_path, tool_list, branch):
    # TODO
    return True


def run_pipeline(jenkins: Jenkins, pipeline_name, *args):
    # *args here is build parameters
    job_instance = jenkins.build_job(pipeline_name, *args)

    return "runPipeline Succeed!"


def create_multibranch_pipeline():
    pass
