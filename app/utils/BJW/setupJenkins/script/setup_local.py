import subprocess
from pathlib import Path

def mkdirs(dir):
    dirs = dir.split('/')
    for i, _ in enumerate(dirs):
        subprocess.call('mkdir ' + '/'.join(dirs[:i]), shell=True)

class SetupLocal:
    path = Path(__file__).parent.absolute() / 'shell'
    path = str(path)

    setup = path + '\\setup.sh'
    run = path + '\\run.sh'

    def __init__(self):
        mkdirs(self.path)

        self._run_sh(self.setup)

        self._build()

        self._run_sh(self.run)

    def _run_sh(self, dir):
        # run setup.sh
        subprocess.call('chmod + x ' + dir, shell=True)
        subprocess.call(r"sed -i 's/\r$//' " + dir, shell=True)
        subprocess.call('./' + dir)
    
    def _build(self):
        print("[+] Building Jenkins docker..")
        subprocess.call('sudo docker build -t bibim-jenkins:0.1 ' + self.path, shell=True)
        subprocess.call('sudo docker volume create jenkins', shell=True)
    





