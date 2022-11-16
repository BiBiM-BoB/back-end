'''OneDayGinger

There are two public fuctions in class JenkinsfileGenerator(),

    [i] generate_by_json()
        (1) tools json -> tools list
        (2) for tool in tools : 
                find groovy(tool)
        (3) concat groovy codes
        (4) generate(groovy)
        (5) git commit & push

    [ii] generate_by_raw_groovy()
        (1) generate(groovy)
        (2) git commit & push

'''

import os
import json

from ...utils.Git_manager import GitManager

class JenkinsfileGenerator(GitManager):
    def __init__(self, local, remote, pipeline_name):
        # set basic jenkins-git property
        super().__init__(local, remote)

        self.pipeline_name = pipeline_name
        self.jenkinsfile_path = "Jenkinsfiles/{pipeline_name}"
    
    def generate_by_json(self, tools_json):
        # json -> list
        self.tool_list = self._json_to_list(tools_json)

        # generate groovy script
        groovy = self._write_stages('FUNC', 'start')
        for tool in self.tool_list:
            groovy += self._write_stages(tool)
        groovy += self._write_stages('FUNC', 'stop')

        # and save it
        self._generate(groovy)

        # git push generated groovy script into jenkins-git
        self.commit_and_push(f'Generated Jenkinsfile "{self.pipeline_name} in {self.jenkinsfile_path}.')

        return self.jenkinsfile_path


    def generate_by_raw_groovy(self, groovy):
        self._generate(groovy)

        return self.jenkinsfile_path

    def _generate(self, groovy: str):
        local_jenkinsfile = str(self.localPath / self.jenkinsfile_path)
        with open(local_jenkinsfile) as f:
            f.write(groovy)
    
    
    def _json_to_list(self, tools_json) -> list:
        tools_list = []
        tools_json = json.loads(tools_json)

        for stage in tools_json.keys():
            for tool in tools_json[stage].keys():
                if tools_json[stage][tool]:
                    tools_list.append(stage + '/' + tool)

        return tools_list

    def _find_stage(self, stage: str, tool_list):
        ret = []
        for tool in tool_list:
            if stage in tool:
                ret.append(tool)
        return ret
        
    # Let's say,
    # self._write_stages('DAST/ZAP')
    def _write_stages(self, tool, part=None):
        # then this function will return Jenkinsfile components about running ZAP, which is variable 'stages' below.
        groovy = ""
        component_dir = self.localgitdir + 'components'
        for dirname, _, files in os.walk(component_dir + tool + '/'):
            print(component_dir + tool)
            files.sort()
            if not part:
                for i in range(len(files)):
                    if int(files[i].split('.')[0]) > 0:
                        files[i:], files[:i] = files[:i], files[i:]
                        break
            
            elif part=='start':
                for i in range(len(files)):
                    if int(files[i].split('.')[0]) > 0:
                        files = files[i:]
                        break
            
            elif part=='stop':
                for i in range(len(files)):
                    if int(files[i].split('.')[0]) > 0:
                        files = files[:i]
                        break

            for f in files:
                f = open(os.path.join(dirname, f), 'r')
                text = f.read()
                
                if text[:6] == "$bibim":
                    f.close()
                    stage_list = self._find_stage(text.split(':')[1], self.tool_list)
                    # if component's content is '$bibim:SCA:start' : self._find_stage will return all sca tool list
                    # for example,
                    # stage_list = ['SCA/Dependabot', 'SCA/Dependency_check']
                    for stage in stage_list:
                        # if component's content is (for example) '$bibim:BUILD:start' : call this func recursively
                        groovy += self._write_stages(stage, text.split(':')[2])
                else:
                    f.close()
                    groovy += text

        return groovy