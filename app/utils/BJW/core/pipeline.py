from api4jenkins import Jenkins
from .generators.JenkinsfileGenerator import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator
import time


def create_pipeline(jenkins: Jenkins, pipeline_name, git_path, tool_json, branch, build_token):
    remotegitdir, jenkinsfile = JenkinsfileGenerator(pipeline_name, tool_json).post_action()
    xml = XMLGenerator(pipeline_name,
                       ("remote", git_path),
                       ("url", remotegitdir),
                       ("remoteJenkinsFile", jenkinsfile),
                       ("name", branch),
                       # ("authToken", build_token)
                       ).post_action()
    
    job_instance = jenkins.create_job(pipeline_name, xml)

    return "createPipeline Succeed!"


def delete_pipeline(jenkins: Jenkins, pipeline_name):
    job_instance = jenkins.delete_job(pipeline_name)
    if jenkins.get_job(pipeline_name):
        return False
    return True


def modify_pipeline(jenkins: Jenkins, pipeline_name, workspace_path, tool_list, branch):
    # TODO
    return True


def run_pipeline(jenkins: Jenkins, pipeline_name, *args):
    # *args here is build parameters
    job_instance = jenkins.build_job(pipeline_name)
    while not job_instance.get_build():
        time.sleep(1)
    print(f"[+] Build {pipeline_name} started!")

    # return job_instance.get_build()

def get_pipeline(jenkins: Jenkins, *args):
    pipeline_list = []
    for job in jenkins.iter_jobs():
        pipeline_list.append(job.full_name)
    return pipeline_list

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
    jenkins = Jenkins("http://localhost:8080", auth=('test', 'test'))
    create_pipeline(jenkins, 'test_pipe_name', "https://github.com/digininja/DVWA", json_obj, "*/master", 'tokensample')