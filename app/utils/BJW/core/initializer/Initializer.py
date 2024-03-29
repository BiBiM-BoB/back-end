'''OneDayGinger

Procedure:

    0. setup local directory if not exists.

    1. download security check tool(clone or pull) 
        from github remote repository "bibim-bob/sectools-completed" into "/home/{user}/bibim/sectools-completed/"

    2. download jenkins-git(clone or pull) 
        from "http://{jenkins}/userContent.git" into "/home/{user}/bibim/userContent/"

    3. update jenkins-git by 
        (1) remove "~/bibim/userContent/sectools/"
        (2) cp "~/bibim/sectools-completed/" into step (1)
        (3) jenkins-git push

    jenkins-git(/userContent):
        |-Jenkinsfiles
        |-xmls
        |-components
            |-groovy
            |-xmls
            |-DAST/ZAP/ ...
        |-debug
'''

import os
import sys
import pathlib
import platform
from distutils import dir_util
from getpass import getuser

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from utils.Git_manager import GitManager

if __name__ == '__main__':
    from ...utils.Git_manager import GitManager


class Initializer:

    user = getuser()

    if platform.system() == 'Linux':
        root = pathlib.PurePosixPath(f'/home/{user}/bibim')
    else:
        root = pathlib.PureWindowsPath(os.path.expanduser('~\\Documents\\bibim'))
    
    sec_git = GitManager(str(root/'sectools-completed'), r"https://github.com/BiBiM-BoB/sectools-completed") # TODO: sec-git init
    
    def __init__(self, jenkins_url, debug=False):
        print("[+] Initializing...")

        if jenkins_url[-1] == r'/':
            self.jenkins_url = jenkins_url + 'userContent.git'
        else:
            self.jenkins_url = jenkins_url + r'/userContent.git'
        self.jenkins_git = GitManager(str(self.root/'userContent'), self.jenkins_url)

        # create bibim folder
        self._setup_dir()

        # clone/pull jenkins-git and sec-git
        updated = False
        if not debug:
            updated = self._setup_git()

        # if sec-git is updated, copy sec-git into jenkins-git, and push
        self._update_jenkins_git()
        
        print("[+] Finished Initializing!")

    def _setup_dir(self):
        try:
            os.makedirs(self.root)
        except FileExistsError:
            print(f"[+] {self.root} already exists!")
    
    def _setup_git(self) -> bool:
        self.jenkins_git.reload()
        flag = self.sec_git.clone_or_pull()

        return flag
    
    def _update_jenkins_git(self):
        # removes all files under /components
        self.jenkins_git.purge('components')

        self._update_worker('components', 'components')
        self._update_worker('jenkins/groovy', 'components/groovy')
        self._update_worker('jenkins/xmls', 'components/xmls')

        self.jenkins_git.commit_and_push('updated git')

    def _update_worker(self, secgit_path, jenkinsgit_path):
        dir_util.copy_tree(
            str(self.sec_git.localPath/secgit_path),
            str(self.jenkins_git.localPath/jenkinsgit_path)
        )

