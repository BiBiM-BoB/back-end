import os
from git import Repo


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
    localgitdir = f'/home/{user}/bibim/resources_git/'

    def commit(self, message):
        commit_all(self.localgitdir, message)

    def post_action(self):
        pass
