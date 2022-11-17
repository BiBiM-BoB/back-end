from script.setup_ec2 import SetupSSH, SetupEC2
from script.setup_local import SetupLocal

def selectSetupMode():
    usage = """
    Setup Jenkins as Docker out of Docker Model.

    Mode 1: Setup Jenkins in local. (ubuntu only)
    Mode 2: Setup Jenkins in EC2. -> gets the name of EC2.
        If EC2 is not found, this module will create new EC2 with that name and setup Jenkins in it.  
    Mode 3: Setup Jenkins by ssh.
    """

    print(usage)
    mode = int(input("Select Setup Mode(1/2/3): "))

    if mode == 1:
        # run script directly
        SetupLocal()

    if mode == 2:
        # 1. create ec2 using boto3
        # 2. connect ec2 via ssh
        # 3. run scripts on ec2
        name = input('[?] Type the name of EC2: ')
        SetupEC2(name)
    
    if mode == 3:
        ip = input("[?] IP address of your target server (xxx.xxx.xxx.xxx): ")
        SetupSSH(name)


if __name__ == "__main__":
    selectSetupMode()