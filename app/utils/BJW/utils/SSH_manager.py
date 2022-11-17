"""OneDayGinger
This file offers various functions for controlling SSH.

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

from . import Interactive as interactive

class SSHManager:
    def __init__(self, ip):
        # prepare ssh connection
        self.ip = ip
        self.ssh = self._establish_ssh()
        self.channel = self._invoke_channel()


    def _establish_ssh(self):
        # connect this computer and target ec2
        # use RSA key verification
        key = paramiko.RSAKey.from_private_key_file(input('[?] Absolute path of your private key file: '))
        username = input('[?] Username of your target server (default: ubuntu): ')
        if not username : username = 'ubuntu'

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.ip, username=username, pkey=key)

        return ssh_client

    def _invoke_channel(self):
        channel = self.ssh.get_transport().open_session()
        channel.get_pty()
        channel.invoke_shell()

        return channel

    def execute_command(self, command, verbose=True):
        _, stdout,_ = self.ssh.exec_command(command)

        if verbose:
            for line in stdout.readlines():
                line = str(line).replace('\n', '')
                print(line)
    
    def execute_channel(self, command, verbose=True):
        self.channel.send(command + '\n')

        while True:
            output = self.channel.recv(1024)
            output = output.decode('utf-8', 'ignore')
            if verbose:
                sys.stdout.write(output)
                sys.stdout.flush()

            if (("ubuntu@" in output) and ("$" in output)) or self.channel.exit_status_ready():
                break
    
    def mkdirs(self, dir):
        dirs = dir.split('/')
        for i,_ in enumerate(dirs):
            self.execute_command('mkdir ' + '/'.join(dirs[:i]), False)

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
        self.mkdirs(cur_dir)
        self.execute_channel('cd ' + cur_dir, True)

        for root, dirs, files in os.walk(from_path):

            for file in files:
                self.upload_file(os.path.join(root ,file), 
                    posixpath.join(cur_dir,file))
                print(f"[+] Uploaded {file}..")

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
    debug.terminate_ec2('TEST_EC2_3')
