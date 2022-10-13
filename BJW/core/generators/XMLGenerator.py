import xml.etree.ElementTree as ET
import shutil
# 이 파일 자체를 실행시키면서 디버깅할때는 from GeneratorBase ~ 가 되어야 함.
from .GeneratorBase import GeneratorBase

class XMLGenerator(GeneratorBase):
    def __init__(self, pipeline_name, *args: tuple):
        self.xml_path = self.localgitdir + "xmls/" + pipeline_name + ".xml"

        self.target_xml = self.copyXML()
        self.root = self.target_xml.getroot()

        self.replace_contents(*args)
        self.finishXML()

        self.commit(f"Generated {pipeline_name}.xml")

    def copyXML(self):
        shutil.copyfile(self.localgitdir + "xmls/config.xml", self.xml_path)
        return ET.parse(open(self.xml_path, 'r', encoding='utf-8'))

    def finishXML(self):
        with open(self.xml_path, 'rt', encoding='UTF-8') as file:
            x = file.read()
        with open(self.xml_path, 'wt', encoding='UTF-8') as file:
            x = "<?xml version='1.0' encoding='utf-8'?>\n" + x
            file.write(x)

    def replace_content(self, target_tag, value):
        it = self.root.iter(target_tag)
        for target in it:
            original = target.text
            modified = original.replace("$bibim", value)

            target.text = modified
        self.target_xml.write(self.xml_path, method='html', encoding='utf-8', xml_declaration=True)

    def replace_contents(self, *args):
        for item in args:
            self.replace_content(item[0], item[1])

    def post_action(self):
        xml = open(self.xml_path, 'r').read()
        return xml

if __name__ == "__main__":
    test = XMLGenerator('test_pipe_name',
                       ("remote", "https://github.com/digininja/DVWA"),
                       ("url", "/home/ubuntu/bibim/JJJJJ"),
                       ("remoteJenkinsFile", "path_inside_git"),
                       ("name", "*/master")).post_action()
    print("DEBUGGING..")