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


Purpose: 이 파이썬 파일은 최신 Security tools git으로부터 jenkins에 필요한 부분들을 추출하여 Jenkins-git에 업로드하는 역할을 한다.

    (1) Jenkins는 내부 정책상 jenkinsfile을 git에서만 가져온다. (확실)
        (1-1) Jenkinsfile은 pipeline의 과정 그 자체를 정의하는 파일이다.
        (1-2) Jenkinsfile의 문법은 declarative, scripted(groovy)의 두가지가 있다.
        (1-3) Declarative는 전통적인 ci/cd 과정에 잘 어울리지는 않으며, 구체적인 동작 정의가 어렵다는 큰 단점이 존재한다. (튜링완전하지 않음)
            => 문법을 scripted(groovy)로 fix한다.
        (1-4) Jenkinsfile은 여러개의 stages로 구성된다. ex) stage('DAST'), stage('BUILD'), ...

    (2) bibim 프로젝트는 ci/cd의 완전 자동화가 가능해야한다.
        (2-1) 유저는 원하는 security tool을 선택한다.
        (2-2) Jenkinsfile은 유저가 선택한 툴들의 조합이다. ex) zap, dependency check, ...
        (2-3) 따라서 Jenkinsfile에 들어갈 groovy 코드를 stage 단위로 작성을 해놓아야 한다.

    => stage 단위로 security tools를 작동시킬 groovy code를 작성하고, 이를 git으로 관리해야 한다.
        - stage 는 다시 groovy code와, 그 groovy code가 작동시키는 security check tool docker으로 구성된다.
        - 즉, stage = {groovy code, dockerfile, (shell codes)}
        
        Jenkins-git은 어떻게 세팅되었는지, git 디렉터리 구조에 대한 근거는 다른 파일에 적어놓겠다.
    
    (3) Tool 팀이 관리하는 통합된 security check tools git은 bibim-bob/back-end가 아닌 아예 새로운 git 디렉터리에 관리되는 것이 올바르다.
        => 현재 분리된 채로 관리되고 있는 security check git의 완성-통합 git을 새로 구축하고, BJW의 debug 기능을 통해 자동으로 쉽게 업데이트 되도록 한다.

    (4) 그렇다면, (1)을 만족시키기 위해 (3)에 해당하는 git을 그대로 사용하면 되지 않는가?
        => 아니다. security tools git는 Jenkins뿐 아니라 다른 ci/cd 툴들에도 사용되므로 추후 용량이 매우 방대해질 것이고,
            제한된 자원으로 작동하는 Jenkins에 그대로 적용하는 것은 매우 비효율적이다.
    
    => 따라서 Jenkins git과 Security tools git을 분리하고, 
        Jenkins git은 오직 Jenkins 서버에만 존재하는 Security tools git의 한 부분에 전적으로 의존해야 한다.(항상 최신 상태를 유지해야 함)

    즉, 이 파이썬 파일은 최신 Security tools git으로부터 jenkins에 필요한 부분들을 추출하여 Jenkins-git에 업로드하는 역할을 한다.

'''

import os
import pathlib
import shutil
import platform

from ...utils.Git_manager import GitManager
# TODO: setup에 git clone 포함

class Initializer:

    user = os.getlogin()

    if platform.system() is 'Linux':
        root = pathlib.PurePosixPath(f'/home/{user}/bibim')
    else:
        root = pathlib.PureWindowsPath(f'C:\\Program Files\\bibim')
    
    sec_git = GitManager(str(root/'sectools-completed'), r"http://github.com/") # TODO: sec-git init
    
    def __init__(self, jenkins_url):
        print("[+] Initializing...")

        if jenkins_url[-1] is r'/':
            self.jenkins_url = jenkins_url + 'userContent.git'
        else:
            self.jenkins_url = jenkins_url + r'/userContent.git'
        self.jenkins_git = GitManager(str(self.root/'userContent'), self.jenkins_url)

        # create bibim folder
        self._setup_dir()

        # clone/pull jenkins-git and sec-git
        updated = self._setup_git()

        # if sec-git is updated, copy sec-git into jenkins-git, and push
        if updated:
            self._update_jenkins_git()
        
        print("[+] Finished Initializing!")

    def _setup_dir(self):
        os.makedirs(self.root)
    
    def _setup_git(self) -> bool:
        self.jenkins_git.clone_or_pull()
        flag = self.sec_git.clone_or_pull()

        return flag
    
    def _update_jenkins_git(self):
        os.removedirs(self.jenkins_git.localPath/'jenkins')
        os.removedirs(self.jenkins_git.localPath/'components')
        shutil.copyfile(self.sec_git.localPath/'jenkins', self.jenkins_git.localPath/'jenkins')
        shutil.copyfile(self.sec_git.localPath/'components', self.jenkins_git.localPath/'components')

        self.jenkins_git.commit_and_push('updated git')

