'''OneDayGinger

    XMLGenerator().generate()
        (1) read and copy base xml
        (2) modify base xml by ElementTree
        (3) save new xml into local jenkins-git
        (4) git push

'''

import xml.etree.ElementTree as ET
import shutil
import sys
import os
from collections import deque

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from utils.Git_manager import GitManager


class NoSuchItemError(Exception):
    def __init__(self, item):
        msg = f"No item named {item} exists!"
        super().__init__(msg)

class XMLGenerator(GitManager):
    def __init__(self, local, remote, pipeline_name, base_xml='config.xml'):
        super().__init__(local, remote)
        self.pipeline_name = pipeline_name

        base_xml = f"components/xmls/{base_xml}"
        self.base_xml = str(self.localPath/base_xml)

        xml_path = f"xmls/{pipeline_name}"
        self.xml_path = str(self.localPath/xml_path)

        try:
            os.makedirs(str(self.localPath/'xmls'))
        except FileExistsError:
            print("[+] xmls dir exists.")

    def generate(self, target, target_branch, jenkinsfile_path, *args):
        element_list = [
            ('sources>remote', target),
            ('remoteJenkinsFile', jenkinsfile_path),
            ('remoteJenkinsFileSCM>url', self.remote)
        ]

        self.target_xml = self._copyXML()
        self.root = self.target_xml.getroot()

        self._replace_contents(element_list)
        if args:
            self._replace_contents(*args)
        
        self._finishXML()
        self.commit_and_push(f'Generated xml "{self.pipeline_name} in {self.xml_path}.')

        with open(self.xml_path, 'r') as f:
            xml = f.read()

        return xml

    def _copyXML(self):
        shutil.copyfile(self.base_xml, self.xml_path)
        return ET.parse(open(self.xml_path, 'r', encoding='utf-8'))

    def _finishXML(self):
        with open(self.xml_path, 'rt', encoding='UTF-8') as file:
            x = file.read()
        with open(self.xml_path, 'wt', encoding='UTF-8') as file:
            x = "<?xml version='1.0' encoding='utf-8'?>\n" + x
            file.write(x)

    def _replace_content(self, target_tag, value):
        if ">" in target_tag:
            target_tag = target_tag.split(">")
            target = self._2_recursive_iter(target_tag[0], target_tag[1])
            for item in target:
                original = item.text
                modified = original.replace('$bibim', value)
                item.text = modified
                self.target_xml.write(self.xml_path, method='html', encoding='utf-8', xml_declaration=True)
            return

        it = self.root.iter(target_tag)
        for target in it:
            original = target.text
            # '$bibim'
            modified = original.replace('$bibim', value)
            target.text = modified
        self.target_xml.write(self.xml_path, method='html', encoding='utf-8', xml_declaration=True)

    def _2_recursive_iter(self, parent, child):
        for items in self.root.iter(parent):
            res = items.iter(child)
        return res


    def _replace_contents(self, *args):
        for item in args[0]:
            self._replace_content(item[0], item[1])
