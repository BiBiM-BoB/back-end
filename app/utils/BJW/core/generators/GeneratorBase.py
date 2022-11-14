import os
from git import Repo
from ..utils.GitManager import push
from dotenv import load_dotenv

load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")


def commit_all(gitdir, commit_message):
    repo = Repo(gitdir)
    try:
        repo.index.add('**')
        repo.index.commit(commit_message)
        print(f"[+] Commited all changed files, commit message:{commit_message}")
    except:
        print("[-] Git commit failed...")
        return False
    return True


class GeneratorBase:
    """Super Class"""
    user = os.getlogin()
    localgitdir = f'/home/{user}/bibim/userContent/'
    remotegitdir = f'{JENKINS_URL}/userContent.git/'

    def _commit(self, message):
        commit_all(self.localgitdir, message)
        push(self.localgitdir)


    def post_action(self):
        pass
