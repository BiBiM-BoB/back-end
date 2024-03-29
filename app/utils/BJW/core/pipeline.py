'''OneDayGinger

# This file controls pipeline directly.

# Call
    Pipeline(jenkins_instance, pipeline_name, branch)

# Properties
    (1) stages -> list
    (2) jenkinsfile -> jenkinsfile_name, jenkinsfile_text
    (3) config -> dictionary
    (4) history
    (5) stream -> Generator

# Functions
    (1) modify -> delete and create pipeline while preserving history
    (2) run -> log stream
    (3) delete

'''

import time
import sys
from typing import Generator

from .config import Config


class Pipeline:
    def __init__(self, jenkins_instance, pipeline_name, branch, token=None):
        self.jenkins = jenkins_instance
        self.pipeline_name = pipeline_name
        self.branch = branch
        self.full_name = pipeline_name + '/' + branch
        self.token = token

    def run(self) -> Generator[str, None, None]:
        """
            Runs this pipeline.

            Return: iterator of a log stream
        """
        job = self.jenkins.build_job(self.full_name)
        while not job.get_build():
            time.sleep(1)
        build = job.get_build()

        return build.progressive_output()

    def delete(self):
        """
            Deletes this pipeline.
        """
        self.jenkins.delete_job(self.full_name)

    def modify(self, target, branch, tool_json=None, groovy=None, token=None, *args):
        self.delete()
        return self.jenkins.create_pipeline(
            self.pipeline_name,
            target, branch, tool_json, groovy, token, args
        )

    def stop(self):
        job = self.jenkins.get_job(self.full_name)
        build = job.get_last_build()
        build.stop()

    @property
    def status(self) -> tuple:
        job = self.jenkins.get_job(self.full_name)
        build = job.get_last_build()

        return build.building, build.result

    @property
    def stream(self):
        return self._get_stream()

    @property
    def jenkinsfile_name(self):
        return self.config['jenkinsfile']

    @property
    def config(self) -> dict:
        return self.get_config()
        
    
    def get_config(self, reload=False) -> dict:
        config = Config(self.jenkins.url, self.pipeline_name, reload=False)
        p = config.jenkins_git.localPath

        ret = dict()
        ret['target_git'] = config['remote']
        ret['branch'] = config['name']
        ret['jenkinsfile'] = config['remoteJenkinsFile'].split('/')[-1]
        ret['jenkinsfile_abs_path'] = str(p/config['remoteJenkinsFile'])

        return ret
    
    def get_metadata(self, config) -> dict:
        path = config['jenkinsfile_abs_path']
        
        status = 'description'
        description = ''
        
        with open(path, 'r', encoding='utf-8') as jenkinsfile:
            metadata = {'jenkinsfile_name': config['jenkinsfile']}
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
        
        metadata['description'] = description
        
        return metadata

    @property
    def overall_data(self) -> dict:
        data = dict(self.get_config())
        data['building'], data['recent_result'] = self.status
        data.update(self.get_metadata(data))
        
        return data

    @property
    def history(self):
        pass

    def _get_stream(self) -> Generator[str, None, None]:
        """
            Gets a log stream.
            If pipeline is not running, then returns last-build's log.

            Return: iterator of a log stream
        """
        job = self.jenkins.get_job(self.full_name)
        build = job.get_last_build()

        return build.progressive_output()

    def __getitem__(self, key):
        return getattr(self, key)
