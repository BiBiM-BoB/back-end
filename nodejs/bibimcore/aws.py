import boto3
import ec2

class AWS:
    def __init__(self):
        self.aws_session = self.configure_aws()
        self.ec2_resource = self.aws_session.resource('ec2')
    
    def configure_aws(self) -> boto3.Session:
        print("[?]AWS access key id? : ", end='')
        _access_key_id = input()
        print("[?]AWS secret access key? : ", end='')
        _secret_access_key = input()
        print("[?]AWS region name? (default : ap-northeast-2) : ", end='')
        self._region_name = input()

        if(not self._region_name):
            self._region_name = 'ap-northeast-2'
        
        session = boto3.Session(
            aws_access_key_id=_access_key_id,
            aws_secret_access_key=_secret_access_key,
            region_name=self._region_name
        )

        return session

    def create_security_group(self, ip, port):
        pass

    def create_ec2(self, key_name, image_id, instance_type, security_group_id, subnet_id, instance_name):
        instances = self.ec2_resource.create_instances(
            KeyName=key_name,
            MinCount=1,
            MaxCount=1,
            ImageId=image_id,
            InstanceType=instance_type,
            SecurityGroupIds=[security_group_id,],
            SubnetId=subnet_id,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ],
        )

        instance_ids = " ".join(str(instance.id) for instance in instances)
        print(f'[+]Created instance {instance_ids}..')
        for instance in instances:
            print(f'[+]Launching instance {instance.id}..')
            instance.wait_until_running()
            print(f'[+]Launched instance {instance.id}!')

        return instances

    def return_ec2(self, instance_id):
        return self.ec2_resource.Instance(instance_id)

    def terminate_ec2(self, instance_id) -> bool:
        try:
            instance = self.ec2_resource.Instance(instance_id)
            instance.terminate()
            print(f'[-]Terminating instance {instance.id}..')
            instance.wait_until_terminated()
            print(f'[+]Instance {instance.id} has been terminated!')

            return True

        except:
            print(f'[!]Failed terminating {instance_id}..')

            return False
    
    def test_session(self) -> bool:
        try:
            instances = self.ec2_resource.instances.all()
            
            instance_num = 0
            for _ in instances:
                instance_num += 1

            print("%d instances existing, session working." % (instance_num))
            return True

        except:
            print("session not working..")
            return False


if __name__ == "__main__":
    my_aws = AWS()
    res = my_aws.test_session()
    instances = my_aws.create_ec2(
        'hskang_key',
        'ami-058165de3b7202099',
        't3a.small',
        'sg-0f0e7ada659706584', # hskang_sg
        'subnet-0960ede25884bc706',
        'BiBiM-Test-new'
    )
    
    input("check if instance created..")

    for instance in instances:

        my_ec2 = ec2.EC2(my_aws.return_ec2(instance.id), 'ubuntu')
        my_ec2.interactive_shell()

        my_aws.terminate_ec2(instance.id)




    