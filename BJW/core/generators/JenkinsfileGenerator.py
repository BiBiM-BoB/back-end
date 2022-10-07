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

tool_order_exception_dict = {
    'ZAP': [('BASE', 1)]
}

import os
import xml.etree.ElementTree as ET

def get_element_by_parent_list(root, parent_list):
    for parent in parent_list:
        root = root.find(parent)
    return root

def init_tools_xml(): 
    root = ET.Element("root")
    rootdir = './resources/tools_components/'

    for dirname, dirnames, filenames in os.walk(rootdir):
        # print path to all filenames.
        if "\\" in dirname:
            parents = dirname[len(rootdir):].split("\\")
        else:
            parents = dirname[len(rootdir):].split('/')
        
        if len(parents)==1 and parents[0]=='':
            for subdirname in dirnames:
                ET.SubElement(root, subdirname)
        elif dirnames:
            print("2: " + str(parents))
            temp = get_element_by_parent_list(root, parents)
            temp.attrib["num"] = str(len(dirnames))
            for subdirname in dirnames:
                ET.SubElement(temp, subdirname)
                # ET.SubElement(parents[-1], subdirname)
        else:
            print("3: " + str(parents))
            get_element_by_parent_list(root, parents).text = str(len(filenames))
    
    with open(rootdir+'tools_test.xml', "wb") as file:
        xml = ET.ElementTree(root)
        xml.write(file, method='html', encoding='utf-8')


def call_generator(tool_list, jenkinsfile_path):
    jenkinsfile = open(jenkinsfile_path, 'w')
    """
    for tool in tool_list:
        print(globals())
        list_buffer = globals()[tool+'_generator']()
        for component in list_buffer:
            component_file = open(library_path+component[0]+'/'+component[1], 'r')
            jenkinsfile.write(component_file.read())
    """
    list_buffer = DAST.ZAP_generator()
    for component in list_buffer:
        component_file = open(library_path + component[0] + '/' + str(component[1]), 'r')
        jenkinsfile.write(component_file.read())


def web_input(input_json):
    tool_list = []

    for stage in input_json:
        for tool in stage:
            if input_json[stage][tool]:
                tool_list.append(stage + '.' + tool)

    call_generator(tool_list)


if __name__ == "__main__":
    # call_generator(['ZAP'], 'test')
    init_tools_xml()