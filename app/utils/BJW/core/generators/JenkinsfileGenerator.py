"""OneDayGinger

"""

import os
import xml.etree.ElementTree as ET
from .GeneratorBase import GeneratorBase
import json

component_dir = "/home/bibim/back-end/app/utils/BJW/core/generators/resources/tools_components/"
# component_dir = os.path.abspath('.') + "/home/bibim/back-end/app/utils/BJW/core/generators/resources/tools_components/"

'''
# Example of input json
json:
{
    'BUILD': {
        'NodeJS': 1,
        'Flask': 0
    }
    'DAST': {
        'ZAP': 1, 
        'Arachni": 0
    },
    'SAST': {
        'CodeQL': 1
    },
    'SCA': {
        'DependencyCheck': 0, 
        'Dependabot': 1
    },
    'SIS': {
        'GGShield': 1,
        'GitLeaks': 1
    }
}

# Example of generated tool_list
tool_list = ['BUILD/NodeJS', 'DAST/ZAP', 'SAST/CodeQL', 'SCA/Dependabot', 'SIS/GGShield', 'SIS/GitLeaks']
'''


def get_element_by_parent_list(root, parent_list):
    for parent in parent_list:
        root = root.find(parent)
    return root


def order_to_file(order):
    # 
    if type(order) == str:
        text = ""
        tool = order.split('/')[-1]
        for dirname, _, files in os.walk(component_dir + order + '/'):
            files.sort()
            for i in range(len(files)):
                if int(files[i].split('.')[0]) > 0:
                    files[i:], files[:i] = files[:i], files[i:]
                    break
            for file in files:
                file = open(os.path.join(dirname, file), 'r')
                text += file.read()
                file.close()
    else:
        file = open(os.path.join(component_dir + order[0], str(order[1])))
        text = file.read()
        file.close()
    return text


class JenkinsfileGenerator(GeneratorBase):
    def __init__(self, pipeline_name, input_json):
        self.pipeline_name = pipeline_name
        self.input_json = input_json

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

        return tool_list

    # Let's say,
    # self._write_stages('DAST/ZAP')
    def _write_stages(self, tool, part=None):
        # then this function will return Jenkinsfile components about running ZAP, which is variable 'stages' below.
        stages = ""

        for dirname, _, files in os.walk(component_dir + tool + '/'):
            files.sort()

            if not part:
                for i in range(len(files)):
                    if int(files[i].split('.')[0]) > 0:
                        files[i:], files[:i] = files[:i], files[i:]
                        break
            
            elif part=='start':
                for i in range(len(files)):
                    if int(files[i].split('.')[0] > 0):
                        files = files[i:]
                        break
            
            elif part=='stop':
                for i in range(len(files)):
                    if int(files[i].split('.')[0] > 0):
                        files = files[:i]
                        break

            for file in files:
                file = open(os.path.join(dirname, file), 'r')
                text = file.read()
                if text[:6] == "$bibim":
                    file.close()
                    stage_list = self._find_stage(text.split(':')[1])
                    # if component's content is '$bibim:SCA:start' : self._find_stage will return all sca tool list
                    # for example,
                    # stage_list = ['SCA/Dependabot', 'SCA/Dependency_check']
                    for stage in stage_list:
                        # if component's content is (for example) '$bibim:BUILD:start' : call this func recursively
                        stages += self._write_stages(stage, text.split(':')[2])
                else:
                    file.close()
                    stages += text
        print(stages)

        return stages

    def _generate_jenkinsfile(self, tool_list):
        jenkinsfile = open(self.jenkinsfile_path, 'w')
        jenkinsfile.write(self._write_stages('FUNC', 'start'))

        for tool in tool_list:
            jenkinsfile.write(self._write_stages(tool))

        jenkinsfile.write(self._write_stages('FUNC', 'stop'))
        jenkinsfile.close()

    def post_action(self):
        return self.remotegitdir, "Jenkinsfiles/" + self.pipeline_name

if __name__ == "__main__":
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
    test = JenkinsfileGenerator('test_pipeline_name', json_obj)
    print("DEBUGGING")