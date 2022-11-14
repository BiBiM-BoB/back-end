from git import Repo


class GitManager:
    def __init__(self, local, remote=None):
        self.remote = remote
        self.local = local
    
    def clone(self):
        repo = Repo.clone_from(self.remote, self.local)

        print(f"[+] Cloned from {self.remote}, into {self.local}")
    
    def pull(self):
        repo = Repo(self.local)
        repo.remotes.origin.pull()

        print(f"[+] Pulled into {self.local}")
    
    def commit(self, message):
        repo = Repo(self.local)
        repo.index.add('**')
        repo.index.commit(message)

        print(f"[+] Commited all changed files in {self.local}, commit message: {message}")
    
    def push(self):
        repo = Repo(self.local)
        repo.remotes.origin.push()

        print(f"[+] Pushed all changes in {self.local}")
