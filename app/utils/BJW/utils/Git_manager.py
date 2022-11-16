from git import Repo
from git.remote import FetchInfo
from git.exc import GitCommandError

from pathlib import Path

class GitManager:
    def __init__(self, local, remote=None):
        self.local = local
        self.remote = remote
        self.localPath = Path(local)
        self.remotePath = Path(remote)
    
    def clone(self):
        repo = Repo.clone_from(self.remote, self.local)

        print(f"[+] Cloned from {self.remote}, into {self.local}")
    
    def pull(self) -> FetchInfo.flags:
        repo = Repo(self.local)
        info = repo.remotes.origin.pull()

        return info[0].flags # https://gitpython.readthedocs.io/en/stable/reference.html?#git.remote.FetchInfo

    def commit(self, message):
        repo = Repo(self.local)
        repo.index.add('**')
        repo.index.commit(message)

        print(f"[+] Commited all changed files in {self.local}, commit message: {message}")
    
    def push(self):
        repo = Repo(self.local)
        repo.remotes.origin.push()

        print(f"[+] Pushed all changes in {self.local}")
    
    def clone_or_pull(self) -> bool:
        try:
            self.clone()

        except GitCommandError: # if already cloned, pull
            flag = self.pull()
        
            if flag is FetchInfo.HEAD_UPTODATE: # if git is up-to-date
                return False
        
        return True
    
    def commit_and_push(self, message):
        self.commit(message)
        self.push()