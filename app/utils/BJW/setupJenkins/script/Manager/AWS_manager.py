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
    def __init__(self):
        self._aws_session = self._configure_aws()

    def _configure_aws(self) -> boto3.Session:
        self._access_key = input("AWS access key: ")
        self._secret_access_key = input("AWS secret access key: ")
        self._region_name = input("AWS region name (default: ap-northeast-2): ")

        if not self._region_name:
            self._region_name = 'ap-northeast-2'

        session = boto3.Session(
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_access_key,
            region_name=self._region_name,
        )

        return session

    def create_ec2(self, instance_name, key_name,
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

    def return_ec2(self, instance_name):

        def get_name(instance):
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    return tag['Value']
        
        ec2_resource = self._aws_session.resource('ec2')
        instances = ec2_resource.instances.filter(Filters=[{'Name': 'tag-key', 'Values': ['Name']}])

        for instance in instances:
            if get_name(instance) == instance_name:
                 print(f"EC2 {instance_name} found! ID: {instance.id}")
                 return instance
        
        print(f"No EC2 named {instance_name} found..")
        return None

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
    
    def test_session(self) -> bool:
        try:
            instances = self._aws_session.resource('ec2').instances.all()

        except Exception as e:
            print("Session not working..")
            return False

        sum = 0
        for _ in instances:
            sum += 1
        print(f'{sum} instances existing, session working.')
        return True

if __name__ == "__main__":
    debug = AWSManager()