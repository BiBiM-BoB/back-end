import os
import json

from .GeneratorBase import GeneratorBase

'''
    1. Creates Jenkinsfile
    2. Commit to local git
    3. Push to origin
'''

class JenkinsfileGenerator(GeneratorBase):
    def __init__(self, pipeline_name, input_json):
        self.pipeline_name = pipeline_name
        self.input_json = json.dumps(input_json)
        self.jenkinsfile_path = self.localgitdir + "Jenkinsfiles/" + pipeline_name

        self.tool_list = self._json_to_list(self.input_json)

        self._generate_jenkinsfile(self.tool_list)
        self._commit(f"Generated Jenkinsfile {pipeline_name}")

    def _find_stage(self, stage: str, tool_list):
        ret = []
        for tool in tool_list:
            if stage in tool:
                ret.append(tool)
        return ret
    
    def _json_to_list(self, input_json):
        tool_list = []

        input_json = json.loads(input_json)

        for stage in input_json.keys():
            for tool in input_json[stage].keys():
                if input_json[stage][tool]:
                    tool_list.append(stage + '/' + tool)
        print(tool_list)
        return tool_list

    # Let's say,
    # self._write_stages('DAST/ZAP')
    def _write_stages(self, tool, part=None):
        # then this function will return Jenkinsfile components about running ZAP, which is variable 'stages' below.
        stages = ""
        component_dir = self.localgitdir + 'components/'
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

            for file in files:
                file = open(os.path.join(dirname, file), 'r')
                text = file.read()
                print(text)
                if text[:6] == "$bibim":
                    file.close()
                    stage_list = self._find_stage(text.split(':')[1], self.tool_list)
                    # if component's content is '$bibim:SCA:start' : self._find_stage will return all sca tool list
                    # for example,
                    # stage_list = ['SCA/Dependabot', 'SCA/Dependency_check']
                    for stage in stage_list:
                        # if component's content is (for example) '$bibim:BUILD:start' : call this func recursively
                        stages += self._write_stages(stage, text.split(':')[2])
                else:
                    file.close()
                    stages += text

        return stages

    def _generate_jenkinsfile(self, tool_list):
        jenkinsfile = open(self.jenkinsfile_path, 'w')
        jenkinsfile.write(self._write_stages('FUNC', 'start'))

        for tool in tool_list:
            print(tool)
            jenkinsfile.write(self._write_stages(tool))

        jenkinsfile.write(self._write_stages('FUNC', 'stop'))
        jenkinsfile.close()

    def post_action(self):
        return self.remotegitdir, "Jenkinsfiles/" + self.pipeline_name