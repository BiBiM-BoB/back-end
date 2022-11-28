from pathlib import Path
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from utils.AWS_manager import AWSManager
from utils.SSH_manager import SSHManager


def SetupEC2(name):
    aws = AWSManager()
    ec2 = aws.return_ec2(name)
    # save basic information of ec2

    if not ec2:
        # if ec2 is not found,
        print('[!] EC2 not found, creating new EC2 instance.')

        key = input('[?] Type the name of AWS private key - for ssh connection (default: bibim_key): ')
        aws.create_ec2(name, key_name=key)
        ec2 = aws.return_ec2(name)

    setup = SetupSSH(ec2.public_ip_address)


class SetupSSH:

    def __init__(self, ip):
        self.ip = ip

        # 1. Connect to instance
        self._connect_SSH()

        # 3. Upload essential setup scripts to instance
        self._upload_files()

        # 4. Run setup shell codes
        self._setup()

        # 5. Run jenkins
        self._run_jenkins()

        # 6. Return instance informations
        self._post_action()

    def _connect_SSH(self):
        self.instance = SSHManager(self.ip)
        self.username = self.instance.username
        self.setup_directory = f'/home/{self.username}/setup/'

    def _upload_files(self):
        path = Path(__file__).parent.absolute()
        path /= 'shell'
        print(f"[+] Uploading setup files from {str(path)}...")
        self.instance.upload_directory(str(path), self.setup_directory)

    def _setup(self):
        print("[+] Setting up prerequired-packages..")
        self.instance.execute_channel('cd ' + self.setup_directory)
        self.instance.execute_channel('ls -al')
        self.instance.execute_channel('chmod +x setup.sh', False)
        self.instance.execute_channel(r"sed -i 's/\r$//' setup.sh")
        self.instance.execute_channel('./setup.sh')

    def _run_jenkins(self):
        print("[+] Running Jenkins...")
        self.instance.execute_channel('chmod +x run.sh', False)
        self.instance.execute_channel(r"sed -i 's/\r$//' run.sh")
        self.instance.execute_channel('./run.sh')

    def _post_action(self):
        print("[+] Install finished ..")
        print(f"[+] Your Server IP: {self.ip}")


if __name__ == "__main__":
    SetupEC2('TEST_EC2_5')
