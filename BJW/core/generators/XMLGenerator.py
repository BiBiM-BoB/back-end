import xml.etree.ElementTree as ET
import shutil
from GeneratorBase import GeneratorBase

class XMLGenerator(GeneratorBase):
    def __init__(self, pipeline_name, *args: tuple):
        self.xml_path = self.localgitdir + "xmls/" + pipeline_name + ".xml"

        self.target_xml = self.copyXML()
        self.root = self.target_xml.getroot()

        self.replace_contents(*args)

        self.commit(f"Generated {pipeline_name}.xml")

    def copyXML(self):
        shutil.copyfile("resources/config.xml", self.xml_path)
        return ET.parse(open(self.xml_path, 'rt', encoding='UTF8'))

    def replace_content(self, target_tag, value):
        it = self.root.iter(target_tag)
        for target in it:
            original = target.text
            modified = original.replace("bibim", value)

            target.text = modified
        self.target_xml.write(self.xml_path)

    def replace_contents(self, *args):
        for item in args:
            self.replace_content(item[0], item[1])

    def post_action(self):
        return self.xml_path