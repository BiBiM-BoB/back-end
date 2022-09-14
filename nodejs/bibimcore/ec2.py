import posixpath
import paramiko
try:
    from bibimcore import interactive
except:
    import interactive
import sys
import os


class EC2:
    def __init__(self, ec2_instance, username):
        self.ec2 = ec2_instance
        self.ssh_client = self.connect_ssh(username)
        self.channel = self.invoke_channel()
        self.init_command()

    def connect_ssh(self, username):
        key = paramiko.RSAKey.from_private_key_file(".\\credential\\hskang_key.pem")
        
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        sshClient.connect(self.ec2.public_ip_address, username=username, pkey=key)
    
        return sshClient
        
    def invoke_channel(self):
        channel = self.ssh_client.get_transport().open_session()
        channel.get_pty()
        channel.invoke_shell()
        return channel

    def interactive_shell(self):
        channel = self.channel

        interactive.interactive_shell(channel)
        self.ssh_client.close()

    def init_command(self):
        self.channel.send('pwd\n')
        counter = 0
        while counter < 2:
            output = self.channel.recv(1024)
            output = output.decode('utf-8', 'ignore')

            if ("ubuntu@" in output) and ("$" in output):
                counter += 1

    def execute_command(self, command, verbose):
        
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
            
    def upload_file(self, from_path, to_path):
        sftp = self.ssh_client.open_sftp()
        sftp.put(from_path, to_path)
    
    def upload_path(self):
        dfs = []
        cur_dir = "/home/ubuntu/bibim/"
        from_path = input("[?]Where is your project dir? : ")

        self.execute_command('mkdir bibim', False)
        self.execute_command('cd ' + cur_dir, False)
        self.execute_command('rm -rf *', False)

        for root, dirs, files in os.walk(from_path):
            
            for file in files:
                print("[*]uploading : " + os.path.join(root, file))
                # print("towards : " + posixpath.join(cur_dir, file))

                self.upload_file(os.path.join(root ,file), posixpath.join(cur_dir,file))
            
            if dirs:
                dirs.reverse()
                for dir in dirs:
                    self.execute_command('mkdir ' + dir, False)
                dfs = [posixpath.join(cur_dir,dirs[i]) for i in range(len(dirs))] + dfs
            else:
                self.execute_command('cd ..', False)
            
            if dfs:
                print(dfs)
                cur_dir = dfs.pop(0)
                self.execute_command('cd ' + cur_dir, False)



            
            #1 dfs.append(dirs)
            #2 self.upload_file(os.path.join(root, file))
            #3 self.execute_command('cd ' + dfs[0], False)
            #1 dfs.append(dirs)
            #2 self.upload_file(os.path.join(root, file))