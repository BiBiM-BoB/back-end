"""OneDayGinger
Jenkinsfile Generator

햄들이 완성하신 툴들로 Jenkinsfile을 만들어주는 코드.


기능 : BJW/core/resources/tools_components 내부의 잘 짜여진 구조에 맞춰
아래와 같이 groovy stage를 작성하시면, 별다른 것 할 필요 없이 알아서 툴이 적용됩니다.


=====================stage example========================
# ./tools_components/DAST/ZAP/2.Execute_ZAP.groogy

stage('Execute ZAP') {
    exec('bibim-zap', 'mkdir /zap/wrk')
    exec('bibim-zap', 'zap-full-scan.py -t http://112.167.178.26:3000 -J /zap/wrk/report.json')
}
==========================================================

일반적으로는 tools_components 내부 groovy의 숫자 순서대로 jenkinsfile이 작성되지만, 커스터마이징이 필요한 경우
아래의 전역변수 tool_order_exception_에 그 순서를 기입해주세요.

"""

import os
import xml.etree.ElementTree as ET
from .GeneratorBase import GeneratorBase
import json

tool_order_exception_dict = {
    'ZAP': [('BUILD/NodeJS', 1), ('BUILD/NodeJS', 2), 'DAST/ZAP', ('BUILD/NodeJS', -1)]
}

component_dir = os.path.abspath('.') + "/core/generators/resources/tools_components/"


def json_to_list(input_json):
    tool_list = []

    input_json = json.loads(input_json)

    for stage in input_json.keys():
        for tool in input_json[stage].keys():
            if input_json[stage][tool]:
                tool_list.append(stage + '/' + tool)

    return tool_list

def get_element_by_parent_list(root, parent_list):
    for parent in parent_list:
        root = root.find(parent)
    return root


def init_tools_xml():
    root = ET.Element("root")

    for dirname, dirnames, filenames in os.walk(component_dir):
        # print path to all filenames.
        if "\\" in dirname:
            parents = dirname[len(component_dir):].split("\\")
        else:
            parents = dirname[len(component_dir):].split('/')

        if len(parents) == 1 and parents[0] == '':
            for subdirname in dirnames:
                ET.SubElement(root, subdirname)
        elif dirnames:
            temp = get_element_by_parent_list(root, parents)
            temp.attrib["num"] = str(len(dirnames))
            for subdirname in dirnames:
                ET.SubElement(temp, subdirname)
                # ET.SubElement(parents[-1], subdirname)
        else:
            get_element_by_parent_list(root, parents).text = str(len(filenames))

    with open(component_dir + 'tools.xml', "wb") as file:
        xml = ET.ElementTree(root)
        xml.write(file, method='html', encoding='utf-8')


def order_to_file(order):
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
        # init tools.xml
        init_tools_xml()
        self.pipeline_name = pipeline_name
        self.jenkinsfile_path = self.localgitdir + "Jenkinsfiles/" + pipeline_name
        self.tool_list = json_to_list(input_json)

        self.generate_jenkinsfile(self.tool_list)
        self.commit("Generated Jenkinsfile {pipeline_name}")


    def generate_jenkinsfile(self, tool_list):
        jenkinsfile = open(self.jenkinsfile_path, 'w')
        jenkinsfile.write(order_to_file(('FUNC', 1)))

        for tool_path in tool_list:
            tool = tool_path.split('/')[-1]
            if tool not in tool_order_exception_dict.keys():
                jenkinsfile.write(order_to_file(tool_path))
            else:
                order_list = tool_order_exception_dict[tool]
                for order in order_list:
                    jenkinsfile.write(order_to_file(order))

        jenkinsfile.write(order_to_file(('FUNC', -1)))
        jenkinsfile.close()

    def post_action(self):
        return self.localgitdir, "Jenkinsfiles/" + self.pipeline_name

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