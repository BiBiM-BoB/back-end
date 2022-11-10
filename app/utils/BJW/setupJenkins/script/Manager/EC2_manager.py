"""OneDayGinger
This file offers various functions for controlling EC2.

Function List:
    COMMAND----------------------
    |   1. execute_command()
    |   2. execute_channel()
    |   3. interactive_commandline()
    UPLOAD-----------------------
    |   4. upload_file()
    |   5. upload_directory()

"""

import posixpath
import paramiko
import sys
import os

import Interactive as interactive

class EC2Manager:
    def __init__(self, ec2_instance):
        # prepare ssh connection
        self.ec2 = ec2_instance
        self.ssh = self._establish_ssh()
        self.channel = self._invoke_channel()


    def _establish_ssh(self):
        # connect this computer and target ec2
        # use RSA key verification
        key = paramiko.RSAKey.from_private_key_file(input('[?] Absolute path of your private key file: '))
        username = input('[?] Username of your ec2 account (default: ubuntu): ')
        if not username : username = 'ubuntu'

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.ec2.public_ip_address, username=username, pkey=key)

        return ssh_client

    def _invoke_channel(self):
        channel = self.ssh.get_transport().open_session()
        channel.get_pty()
        channel.invoke_shell()

        return channel

    def execute_command(self, command, verbose: bool):
        _, stdout,_ = self.ssh.exec_command(command)

        if verbose:
            for line in stdout.readlines():
                line = str(line).replace('\n', '')
                print(line)
    
    def execute_channel(self, command, verbose: bool):
        self.channel.send(command + '\n')

        while True:
            output = self.channel.recv(1024)
            output = output.decode('utf-8', 'ignore')
            if verbose:
                sys.stdout.write(output)
                sys.stdout.flush()

            if command[-1] == "\\":
                if (">" in output):
                    break
            else:
                if ("ubuntu@" in output) and ("$" in output):
                    break

    def interactive_commandline(self):
        channel = self.channel

        interactive.interactive_shell(channel)
        self.ssh_client.close()

    def upload_file(self, from_path, to_path):
        sftp = self.ssh.open_sftp()
        sftp.put(from_path, to_path)

    def upload_directory(self, from_path, to_path):
        # use dfs
        dfs = []
        cur_dir = to_path
        self.execute_channel('cd ' + cur_dir, False)

        for root, dirs, files in os.walk(from_path):

            for file in files:
                self.upload_file(os.path.join(root ,file), 
                    posixpath.join(cur_dir,file))

            if dirs:
                for dir in dirs.reverse():
                    self.execute_channel('mkdir ' + dir, False)
                    dfs = [posixpath.join(cur_dir,dirs[i]) for i in range(len(dirs))] + dfs
            else:
                self.execute_channel('cd ..', False)
            
            if dfs:
                cur_dir = dfs.pop(0)
                self.execute_channel('cd ' + cur_dir, False)
        
        # check if correctly uploaded
        self.execute_command('ls -al '+ to_path, True)

if __name__ == "__main__":
    from AWS_manager import AWSManager
    import logging

    logging.basicConfig()
    logging.getLogger("paramiko").setLevel(logging.DEBUG)

    debug = AWSManager()
    test = EC2Manager(debug.return_ec2('TEST_EC2'))
    test.upload_directory('C:\\dev\\study_bob\\git\\jinho_syshack\\bob11-master\\lec1', '/home/ubuntu/')
    test.interactive_commandline()
