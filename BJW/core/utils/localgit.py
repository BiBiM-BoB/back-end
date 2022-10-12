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
        print("[+] Commited all changed files.")
    except:
        print("[-] Git commit failed...")
        return False
    return True


if __name__ == "__main__":
    create_git("eh")
