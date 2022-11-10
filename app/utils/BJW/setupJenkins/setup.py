
def selectSetupMode():
    usage = """
    Setup Jenkins as Docker out of Docker Model.

    Mode 1: Setup Jenkins in local.
    Mode 2: Create EC2 and setup Jenkins there.
    Mode 3: Setup Jenkins in existing EC2.
    """

    print(usage)
    mode = int(input("Select Setup Mode(1/2/3): "))

    if mode == 1:
        # run script directly
        pass

    if mode == 2:
        # 1. create ec2 using boto3
        # 2. connect ec2 via ssh
        # 3. run scripts on ec2
        pass

    if mode == 3:
        # 1. connect ec2 via ssh
        # 2. run scripts on ec2
        pass

if __name__ == "__main__":
    selectSetupMode()