from jenkinsapi.jobs import Jobs
from generators import JenkinsfileGenerator, XMLGenerator


def create_pipeline(jenkins, pipeline_name, workspace_path, tool_list, branch, token):
    jenkinsfile = JenkinsfileGenerator.json_to_list(workspace_path, tool_list)
    xml = XMLGenerator(pipeline_name, workspace_path, jenkinsfile, branch, token)
    job_instance = Jobs(jenkins).create(pipeline_name, xml.target_xml_path)

    return "createPipeline Succeed!"


def create_multibranch_pipeline():
    pass
