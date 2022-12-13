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

    @property
    def status(self) -> tuple:
        job = self.jenkins.get_job(self.full_name)
        build = job.get_last_build()

        return build.building, build.result

    @property
    def stream(self):
        return self._get_stream()

    @property
    def stages(self):
        with open(self.config['jenkinsfile_abs_path'], 'r', encoding='utf-8') as f:
            firstline = f.readline()
            stage_list = firstline.lstrip('// ').split(', ')
        return stage_list

    @property
    def jenkinsfile_name(self):
        return self.config['jenkinsfile']

    @property
    def config(self) -> dict:
        config = Config(self.jenkins.url, self.pipeline_name)
        p = config.jenkins_git.localPath

        ret = dict()
        ret['target_git'] = config['remote']
        ret['branch'] = config['name']
        ret['jenkinsfile'] = config['remoteJenkinsFile'].split('/')[-1]
        ret['jenkinsfile_abs_path'] = str(p/config['remoteJenkinsFile'])

        return ret

    @property
    def overall_data(self) -> dict:
        data = self.config
        data['stages'] = self.stages
        data['building'], data['recent_result'] = self.status
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
