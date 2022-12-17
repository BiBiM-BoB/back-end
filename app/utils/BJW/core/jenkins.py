'''OneDayGinger

# Properties
    (1) pipeline_list

# Functions
    (1) create_pipeline -> Pipeline
    (2) get_pipeline -> Pipeline
    (3) generate_new_api_token -> str
'''

import api4jenkins
import os
import sys
from getpass import getuser
import platform
import pathlib
from api4jenkins.job import WorkflowJob

from .pipeline import Pipeline
from .initializer.Initializer import Initializer
from .generators.JenkinsfileGenerator import JenkinsfileGenerator
from .generators.XMLGenerator import XMLGenerator

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from utils.Git_manager import GitManager


class PipelineExistsError(Exception):
    def __init__(self, pipeline_name, branch):
        msg = f"Pipeline {pipeline_name} / {branch} already exists!"
        super().__init__(msg)


class Jenkins(api4jenkins.Jenkins):
    user = getuser()

    if platform.system() == 'Linux':
        root = pathlib.PurePosixPath(f'/home/{user}/bibim')
    else:
        root = pathlib.PureWindowsPath(os.path.expanduser('~\\Documents\\bibim'))
        
    def __init__(self, url, username, token):
        super().__init__(url, auth=(username, token))
        
        if url[-1] == r'/':
            self.jenkins_url = url + 'userContent.git'
        else:
            self.jenkins_url = url + r'/userContent.git'
        self.jenkins_git = GitManager(str(self.root/'userContent'), self.jenkins_url)

    def create_pipeline(self, 
                        pipeline_name, 
                        target, 
                        target_branch, 
                        tool_json=None, 
                        jenkinsfile_name=None, 
                        groovy=None, 
                        debug=False, 
                        token=None, 
                        *args, **kwargs) -> Pipeline:

        #  check if pipeline already exists
        if pipeline_name in self.get_pipelines(simple=True):
            raise PipelineExistsError(pipeline_name, target_branch)

        # 0. Init gits
        initializer = Initializer(self.url, debug)

        # 1. create Jenkinsfile according to tool_json
        JG = JenkinsfileGenerator(
            initializer.jenkins_git.local,
            initializer.jenkins_git.remote,
            pipeline_name,
            jenkinsfile_name
        )
        if tool_json:
            jenkinsfile = JG.generate_by_json(tool_json, **kwargs)
        if groovy:
            jenkinsfile = JG.generate_by_raw_groovy(groovy, **kwargs)

        # 2. create config.xml
        XG = XMLGenerator(
            initializer.jenkins_git.local,
            initializer.jenkins_git.remote,
            pipeline_name
        )
        xml = XG.generate(target, target_branch, jenkinsfile)

        # 3. create pipeline with that two files
        job = self.jenkins.create_job(pipeline_name, xml)

        return Pipeline(self, pipeline_name, target_branch, token)

    def get_pipeline(self, pipeline_name, branch, token=None) -> Pipeline:
        return Pipeline(self, pipeline_name, branch, token)

    @property
    def jenkinsfiles(self) -> dict:
        return self.get_jenkinsfiles()
    
    @property
    def pipeline_list(self) -> list:
        return self.get_pipelines()
    
    def get_jenkinsfiles(self):
        root_dir = str(self.jenkins_git.localPath / 'Jenkinsfiles')
        files = os.listdir(root_dir)
        ret = []
        for f in files:
            status = 'description'
            description = ''
            path = os.path.join(root_dir, f)
            
            with open(path, 'r', encoding='utf-8') as jenkinsfile:
                metadata = {'jenkinsfile_name': f}
                for line in jenkinsfile.readlines():
                    line = line.strip()
                    
                    # '// data'
                    if 'bibim_metadata_start' in line:
                        status = 'start'
                        continue
                    
                    if 'bibim_metadata_end' in line:
                        break
                        
                    if status == 'description':
                        description += line[3:] + '\n'
                    
                    elif status == 'start':
                        key, value = line[3:].split(': ')
                        metadata[key] = value
            metadata['description'] = description
            
            t = metadata['tool_list']
            temp = t[2:-2].split("', '")
            temp_dict = dict()
            for tool in temp:
                a, b = tool.split('/')
                if a in temp_dict.keys():
                    temp_dict[a].append(b)
                else:
                    temp_dict[a] = [b]
            metadata['tool_list'] = dict(temp_dict)
            
            ret.append(metadata)
        
        return ret
            
            
    def get_pipelines(self, simple=False):
        ret = []
        
        if simple:
            for job in self.iter_jobs():
                ret.append(job.name)
        
        else:
            status = "FOUND"
            ban_list = []
            for job in self.iter_jobs(4):
                if type(job) is WorkflowJob:
                    temp = job.full_name.split('/')
                    if temp[0] in ban_list:
                        continue
                    if status == "FOUND":
                        pipeline = self.get_pipeline(temp[0], temp[1])
                        pipeline = pipeline['overall_data']
                    
                    
                    if temp[1] != pipeline['branch']:
                        status = "SEARCHING"
                        
                    if temp[1] == pipeline['branch']:
                        status = "FOUND"
                        pipeline['pipeline_name'] = temp[0]
                        ret.append(pipeline)
                        ban_list.append(temp[0])

        return ret
    
    def get_building(self):
        ret = []
        node = api4jenkins.node.MasterComputer(self, self.url + 'manage/computer/(built-in)/')
        builds = node.iter_building_builds()
        for i in builds:
            ret.append(i.get_job())
        return ret
        
    def __getitem__(self, key):
        return getattr(self, key)
