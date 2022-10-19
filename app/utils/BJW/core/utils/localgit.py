from git import Repo
import os


def create_git(gitdir):
    if not os.path.isdir(gitdir):
        try:
            os.mkdir(gitdir)
        except:
            print("[-] Please run init.py first ...")

    if not os.path.isdir(gitdir + '.git/'):
        repo = Repo.init(gitdir)
    else:
        print("[-] Git already exists ...")


def commit_all(gitdir, commit_message):
    repo = Repo(gitdir)
    try:
        repo.index.add('**')
        repo.index.commit(commit_message)
        print(f"[+] Commited all changed files, commit message: {commit_message}")
    except:
        print("[-] Git commit failed...")
        return False
    return True

def clone_or_pull(gitdir, localdir):
    try:
        repo = Repo.clone_from(gitdir, localdir)
        print(f"[+] Cloned from {gitdir}!")
    except:
        repo = Repo(localdir)
        repo.remotes.origin.pull()
        print(f"[+] Already cloned, so pulled from {gitdir}!")

def push(localdir):
    repo = Repo(localdir)
    try:
        repo.remotes.origin.push()
        print("[+] Pushed all changes!")
    except Exception as e:
        print(f"[-] Push failed, ERROR: {e}...")


if __name__ == "__main__":
    create_git("eh")
