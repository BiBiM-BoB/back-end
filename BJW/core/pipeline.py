from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from .generators import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator


def create_pipeline(jenkins: Jenkins, pipeline_name, git_path, tool_list, branch, build_token):
    jenkinsfile = JenkinsfileGenerator.json_to_list(git_path, tool_list)
    xml = XMLGenerator(("url", git_path),
                       ("projectUrl", git_path),
                       # TODO: jenkinsfile local git management
                       # ("jenkinsfile_path", jenkinsfile),
                       ("name", branch),
                       ("authToken", build_token))
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
