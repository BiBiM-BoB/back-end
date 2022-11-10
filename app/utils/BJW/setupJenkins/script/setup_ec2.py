from pathlib import Path

from .Manager.AWS_manager import AWSManager
from .Manager.EC2_manager import EC2Manager

class SetupEC2:

    setup_directory = '/home/ubuntu/setup/'

    def __init__(self, name):
        # 1. Find EC2 instance
        self.ec2 = self._find_EC2(name)

        # 2. Connect to EC2 instance
        self._connect_EC2()

        # 3. Upload essential setup scripts to EC2
        self._upload_files()

        # 4. Run setup shell codes
        self._setup()
        
        


    def _find_EC2(self, name):
        ec2 = AWSManager().return_ec2(name)

        if not ec2:
            # if ec2 is not found,
            print('[!] EC2 not found, creating new EC2 instance.')

            key = input('[?] Type the name of AWS private key - for ssh connection (default: bibim_key): ')
            ec2 = AWSManager.create_ec2(name, key)

        return ec2
    
    def _connect_EC2(self):
        self.ec2 = EC2Manager(self.ec2)

    def _upload_files(self):
        path = Path(__file__).parent.absolute()
        path += '\\shell\\'
        self.ec2.upload_directory(path, self.setup_directory) # TODO: mkdirs

    def _setup(self):
        self.ec2.execute_channel('cd ' + self.setup_directory, False)
        self.ec2.execute_channel('chmod +x ./setup.sh', False)
        self.ec2.execute_channel('sudo ./setup.sh')