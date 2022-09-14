import bibimcore

def read_bibimfile(ec2):
    directory = input("[?]Where is bibimfile? : ")
    if "Bibimfile" not in directory:
        directory += "\\Bibimfile"
    bibimfile = open(directory, 'r')
    
    lines = bibimfile.readlines()
    for line in lines:
        ec2.execute_command(line, True)


def auto_bibim(ec2_num):
    bibim_aws = bibimcore.AWS()
    
    select = input("[?]Select - New ec2 (1)   Existing ec2 (2) : ")

    if select == '1':
        print("[*]Creating new instance named BiBiM-Test-new ...")
        print("[*]Takes some time ...")
        instances = bibim_aws.create_ec2(
        'hskang_key',
        'ami-058165de3b7202099',
        't3a.small',
        'sg-0f0e7ada659706584', # hskang_sg
        'subnet-0960ede25884bc706',
        'BiBiM-Test-new'
        )
        print("[!]New ec2 created!!!")

        for instance in instances:
            bibim_ec2 = bibimcore.EC2(bibim_aws.return_ec2(instance.id), 'ubuntu')
    else:
        bibim_ec2 = bibimcore.EC2(bibim_aws.return_ec2(ec2_num), 'ubuntu')
    
    bibim_ec2.upload_path()
    read_bibimfile(bibim_ec2)

    bibim_ec2.interactive_shell()

    if select == 1:
        print("[-]Ec2 terminating...")
        bibim_aws.terminate_ec2(instance.id)
        print("[!]Ec2 terminated!!")


if __name__ == "__main__":
    auto_bibim('i-0b3ffec6cf62c2bf7')