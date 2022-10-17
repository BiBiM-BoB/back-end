from .utils.localgit import create_git, commit_all, clone_or_pull, push
import os
import shutil


def create_bibim_folder():
    print("[+] Creating 'bibim' folder ...")
    user = os.getlogin()
    path = f'/home/{user}/bibim/'
    try:
        os.mkdir(path)
        print(f"[+] Created folder on {path}!")
    except:
        print("[-] Folder already exists ...")
        return False
    return path


def create_userContent(jenkinsurl):
    print("[+] Creating local 'bibim' git ...")
    user = os.getlogin()
    path = f'/home/{user}/bibim/userContent/'
    if jenkinsurl[-1] != '/':
        jenkinsurl += '/'
    try:
        clone_or_pull(jenkinsurl + "userContent.git", f'/home/{user}/bibim/userContent')
    except:
        print("[-] Local git already exists ...")

    if not os.path.isdir(path + 'xmls/'):
        os.mkdir(path + 'xmls/')
        shutil.copyfile(os.path.abspath('.') + "/app/utils/BJW/core/generators/resources/config.xml",
                        path + "xmls/config.xml")
        print("[+] Created base config.xml file on git!")
    if not os.path.isdir(path + 'Jenkinsfiles/'):
        os.mkdir(path + 'Jenkinsfiles/')
    if not os.path.isdir(path + 'components/'):
        shutil.copytree(os.path.abspath('.') + "/app/utils/BJW/core/generators/resources/tools_components",
                        path + 'components')

    commit_all(path, "initial commit")


def auto_init(jenkinsurl):
    print("==================== INITIALIZING ====================")
    create_bibim_folder()
    create_userContent(jenkinsurl)
    print("============== Finished initialization! ==============")


if __name__ == "__main__":
    auto_init("http://localhost:8080")
