'''OneDayGinger

    Debug Initializer에는 두가지 모드가 있다.

    1. Debug Mode
        (1) purge files in jenkins-git/debug/
        (2) shutil copyfile in user_input_files into jenkins-git/debug/
        (3) git push
        # (4) ssh -> build given dockerfile (user must give docker name also.)
        # (5) create, run pipeline
        # (6) remove docker image

    2. Push Mode
        (1) git pull sectools
        (2) shutil cp into sectools
        (3) git push

'''
import os
import pathlib
import platform
import sys
from distutils import dir_util

from werkzeug.datastructures import MultiDict, FileStorage

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from utils.Git_manager import GitManager

if __name__ == '__main__':
    from ...utils.Git_manager import GitManager

class DebugInitializer:

    user = os.getlogin()

    if platform.system() == 'Linux':
        root = pathlib.PurePosixPath(f'/home/{user}/bibim')
    else:
        root = pathlib.PureWindowsPath(os.path.expanduser('~\\Documents\\bibim'))

    def __init__(self, jenkins_url):
        if jenkins_url[-1] == r'/':
            self.jenkins_url = jenkins_url + 'userContent.git'
        else:
            self.jenkins_url = jenkins_url + r'/userContent.git'

        self.jenkins_git = GitManager(self.root/'userContent', self.jenkins_url)
        self.sec_git = GitManager(self.root/'sectools-completed', r"https://github.com/BiBiM-BoB/sectools-completed")

        try:
            os.makedirs(str(self.root))
        except FileExistsError:
            pass

        self.jenkins_git.reload()
        self.sec_git.clone_or_pull()

    def debug_mode(self, input_dockerfile: FileStorage, input_script_dir: MultiDict[FileStorage], ssh_key_path=None):
        self._update_jenkins_git()

        # purge jenkins git
        self.jenkins_git.purge('debug')
        self.jenkins_git.mkdirs('debug/Dockerfile')
        self.jenkins_git.mkdirs('debug/script')

        # copy user_input files
        # shutil.copyfile(input_dockerfile, str(self.jenkins_git.localPath / 'debug/Dockerfile'))
        # TODO: secure filename
        try:
            input_dockerfile.save(str(self.jenkins_git.localPath / 'debug/Dockerfile' / input_dockerfile.filename))
        except AttributeError:
            print("[+] No dockerfile..")

        # copy_tree(input_script_dir, str(self.jenkins_git.localPath / 'debug/script'))
        # input_script_dir == flask filestorage list
        try:
            for file in input_script_dir:
                temp = file.filename.split('/')
                temp = "/".join(temp[1:])
                file.save(str(self.jenkins_git.localPath / 'debug/script' / temp))
        except Exception as e:
            print("[+] No scripts..")

        # jenkins-git push
        self.jenkins_git.commit_and_push('Push for debug')

        # ssh docker build, remove after run
        # yet, user must do this manually

    def push_mode(self, groovy_code, groovy_name, input_dockerfile, input_script_dir, stage, tool_name):

        # mkdir
        script_dir = 'components' + '/' + stage + '/' + tool_name + '/script'
        dockerfile_dir = 'components' + '/' + stage + '/' + tool_name
        groovy_dir = 'jenkins/groovy' + '/' + stage + '/' + tool_name

        self.sec_git.mkdirs(
            script_dir,
            groovy_dir
        )
        if input_dockerfile:
            # copy files into secgit
            input_dockerfile.save(str(self.sec_git.localPath / dockerfile_dir / input_dockerfile.filename))
        for file in input_script_dir:
            temp = file.filename.split('/')
            temp = "/".join(temp[1:])
            file.save(str(self.sec_git.localPath / script_dir / temp))

        with open(str(self.sec_git.localPath / groovy_dir / groovy_name), 'w') as f:
            f.write(groovy_code)

        # git push
        self.sec_git.commit_and_push(f"Pushed components of {stage} / {tool_name}")

    def _update_jenkins_git(self):
        # removes all files under /components
        self.jenkins_git.purge('components')

        dir_util.copy_tree(str(self.sec_git.localPath/'components'), str(self.jenkins_git.localPath/'components'))
        dir_util.copy_tree(str(self.sec_git.localPath/'jenkins'/'groovy'), str(self.jenkins_git.localPath/'components/groovy'))
        dir_util.copy_tree(str(self.sec_git.localPath/'jenkins'/'xmls'), str(self.jenkins_git.localPath/'components/xmls'))

        self.jenkins_git.commit_and_push('updated git')

