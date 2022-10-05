from jenkinsapi.jobs import Jobs
from generators import JenkinsfileGenerator, XMLGenerator


def create_pipeline(jenkins, pipeline_name, workspace_path, tool_list, branch, token):
    jenkinsfile = JenkinsfileGenerator.call_generator(pipeline_name, workspace_path, tool_list)
    xml = XMLGenerator(pipeline_name, workspace_path, jenkinsfile, branch, token)
    job_instance = Jobs(jenkins).create(pipeline_name, xml)

    return "createPipeline Succeed!"


def create_multibranch_pipeline():
    pass
