import xml.etree.ElementTree as ET
import shutil
import inspect

class XMLGenerator:
    def __init__(self, *args):
        self.target_xml_path = workspace_dir + xml_name
        self.repository_dir = repository_dir
        self.branch = branch
        self.token = token

        self.target_xml = self.copyXML()
        self.root = self.target_xml.getroot()

        self.auto_set()

    def copyXML(self):
        shutil.copyfile("resources/config.xml", self.target_xml_path)
        return ET.parse(open(self.target_xml_path, 'rt', encoding='UTF8'))

    def replace_content(self, target_tag, value):
        it = self.root.iter(target_tag)
        for target in it:
            original = target.text
            modified = original.replace("bibim", value)

            target.text = modified
        self.target_xml.write(self.target_xml_path)

    # replacing '$bibim' to input values
    # TODO: 커스터마이징이 조금 더 쉽도록 *args, **kargs 형태로 수정

    def replace_contents(self, *args):
    def auto_set(self):
        for attributes in inspect.getmembers(self):
            if attributes[0][:4] == 'set_':
                attributes[1]()

    def set_workspace_dir(self):
        self.replace_content("projectUrl", self.repository_dir)
        self.replace_content("url", self.repository_dir)

    def set_branch(self):
        self.replace_content("name", self.branch)

    def set_token(self):
        self.replace_content("authToken", self.token)

    def check_validity(self):
        return True

if __name__ == "__main__":
    test = XMLGenerator("../", "/iam/just/atest/", "test.xml", "*/master", "testToken")