import boto3
import time
import requests

# Create EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Launch EC2 instance (same as previous code)...
response = ec2_client.run_instances(
    ImageId='ami-0e449927258d45bc4',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='ec2-key-pair',
    SecurityGroupIds=['sg-0786d9d91d9e48b1d'],
    SubnetId='subnet-0e1b29c9b72e49dee',
    UserData='''#!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>Welcome to your EC2 instance!</h1>" > /var/www/html/index.html
    ''',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'MyTestEC2Instance'}
            ]
        }
    ]
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Launched instance: {instance_id}")

# Wait for the instance to be running and get public IP
ec2_resource = boto3.resource('ec2', region_name='us-east-1')
instance = ec2_resource.Instance(instance_id)

print("Waiting for instance to be in 'running' state...")
instance.wait_until_running()
instance.load()

public_ip = instance.public_ip_address
print(f"Public IP: {public_ip}")

# Optional: Wait a bit more for the web server to start
time.sleep(60)

# Call the index.html
try:
    url = f"http://{public_ip}/index.html"
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Page content:\n{response.text}")
except Exception as e:
    print(f"Failed to call the web page: {e}")
