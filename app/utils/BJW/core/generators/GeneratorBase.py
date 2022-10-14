import os
from git import Repo
from ..utils.localgit import push
from dotenv import load_dotenv

load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")


def commit_all(gitdir, commit_message):
    repo = Repo(gitdir)
    try:
        repo.index.add('**')
        repo.index.commit(commit_message)
        print("[+] Commited all changed files.")
    except:
        print("[-] Git commit failed...")
        return False
    return True


class GeneratorBase:
    """Super Class"""
    user = os.getlogin()
    #localgitdir = f'/home/{user}/bibim/resources_git/'
    localgitdir = f'{JENKINS_URL}/userContent.git/'

    def commit(self, message):
        commit_all(f'/home/{self.user}/bibim/userContent', message)
        push(self.localgitdir, f'/home/{self.user}/bibim/userContent')


    def post_action(self):
        pass
