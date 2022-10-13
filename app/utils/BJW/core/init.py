from .utils.localgit import create_git, commit_all
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


def create_resources_git():
    print("[+] Creating local 'bibim' git ...")
    user = os.getlogin()
    path = f'/home/{user}/bibim/resources_git/'
    try:
        create_git(path)
        print(f"[+] Created local git on {path}!")

        os.mkdir(path + 'xmls/')

        os.mkdir(path + 'Jenkinsfiles/')

        commit_all(path, "initial commit")

    except:
        print("[-] Local git already exists ...")

    try:
        shutil.copyfile(os.path.abspath('.') + "/app/utils/BJW/core/generators/resources/config.xml", path + "xmls/config.xml")
        commit_all(path, "put config.xml")
        print("[+] Created base config.xml file on git!")

    except:
        print("[-] Base config.xml already exists ...")
        return False
    return True


def auto_init():
    print("==================== INITIALIZING ====================")
    create_bibim_folder()
    create_resources_git()
    print("============== Finished initialization! ==============")


if __name__ == "__main__":
    auto_init()
