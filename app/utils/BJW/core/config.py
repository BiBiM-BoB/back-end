import platform
import pathlib
import os
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from utils.Git_manager import GitManager

if __name__ == '__main__':
    from ...utils.Git_manager import GitManager


class NoSuchElementError(Exception):
    def __init__(self, element):
        msg = f"There is no element named {element}."
        super().__init__(msg)


class Config:
    user = os.getlogin()

    if platform.system() == 'Linux':
        root = pathlib.PurePosixPath(f'/home/{user}/bibim/userContent/')
    else:
        root = pathlib.PureWindowsPath(os.path.expanduser('~\\Documents\\bibim\\userContent'))

    def __init__(self, jenkins_url, pipeline_name):
        self.jenkins_url = self._url_init(jenkins_url)
        self.jenkins_git = GitManager(str(self.root), self.jenkins_url)
        self.jenkins_git.reload()

        self.filename = pipeline_name + '.xml'
        self.xml_path = str(self.jenkins_git.localPath/f"xmls/{pipeline_name}")
        self.xml_instance = ET.parse(open(self.xml_path, 'r', encoding='utf-8'))
        self.xml_root = self.xml_instance.getroot()

    def _get_element(self, tag):
        text = ""
        it = self.xml_root.iter(tag)
        for target in it:
            text = target.text

        if not text:
            raise NoSuchElementError(tag)

        return text

    @staticmethod
    def _url_init(self, jenkins_url):
        if jenkins_url[-1] == r'/':
            return jenkins_url + 'userContent.git'
        else:
            return jenkins_url + r'/userContent.git'

    def __getitem__(self, key):
        return self._get_element(key)
