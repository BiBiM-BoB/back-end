"""OneDayGinger
This file manages AWS by boto3.

Function List:
    1. createEC2(instance_name:str)
    2. returnEC2() -> None / ec2
    3. terminateEC2()
    4. test_session()

# reference: https://russell.ballestrini.net/filtering-aws-resources-with-boto3/
"""
import boto3


class AWSManager:
    # credential datas
    _access_key = ""
    _secret_access_key = ""
    _region_name = ""

    def __init__(self):
        self._aws_session = self._configure_aws()

    def _configure_aws(self) -> boto3.Session:
        self._access_key = input("AWS access key: ")
        self._secret_access_key = input("AWS secret access key: ")
        self._region_name = input("AWS region name(default : ap-northeast-2): ")

        if not self._region_name:
            self._region_name = 'ap-northeast-2'

        session = boto3.Session(
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_access_key,
            region_name=self._region_name,
        )

        return session

    def create_ec2(self, instance_name: str,
                   key_name='bibim_key',
                   image_id='ami-058165de3b7202099',
                   instance_type='t3a.small',
                   security_group_id='sg-0aea7cc41003b6fcb',  # bibim_sg
                   subnet_id='subnet-0960ede25884bc706'):

        ec2_resource = self._aws_session.resource('ec2')
        targets = ec2_resource.create_instances(
            KeyName=key_name, MinCount=1, MaxCount=1, ImageId=image_id,
            InstanceType=instance_type, SecurityGroupIds=[security_group_id, ],
            SubnetId=subnet_id,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name,
                        }
                    ]
                }
            ],
        )

        for target in targets:
            print(f'[+] Launching instance {instance_name}..')
            target.wait_until_running()
            print(f'[+] Launched instance {instance_name}!')

        return targets[0]

    def return_ec2(self, instance_name) -> boto3.resource('ec2').Instance:
        ec2_resource = self._aws_session.resource('ec2')
        filters = [{'Name': 'tag:Name', 'Values': instance_name}]
        instances = ec2_resource.instances.filter(Filters=filters)

        if not instances:
            print(f"No EC2 named {instance_name} found..")
            return None

        print(f"EC2 {instance_name} found! ID: {instances[0].id}")
        return instances[0]

    def terminate_ec2(self, instance_name) -> bool:
        instance = self.return_ec2(instance_name)

        if not instance:
            return False

        print(f'Terminating instance {instance.id}..')
        instance.terminate()

        try:
            instance.wait_until_terminated()
            print(f'Instance {instance.id} has been terminated!')
            return True
        except Exception as e:
            print(e)
            return False

