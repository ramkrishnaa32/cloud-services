import boto3
import time
import requests
import base64

# Load your custom index.html file
with open('../index.html', 'r') as f:
    html_content = f.read()

# Escape the content for shell and embed in user data
user_data_script = f'''#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
cat > /var/www/html/index.html <<EOF
{html_content}
EOF
'''

# Create EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Launch EC2 instance
response = ec2_client.run_instances(
    ImageId='ami-0e449927258d45bc4',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='ec2-key-pair',
    SecurityGroupIds=['sg-0786d9d91d9e48b1d'],
    SubnetId='subnet-0e1b29c9b72e49dee',
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'CustomWebServer'}]
        }
    ]
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Launched instance: {instance_id}")

# Wait until the instance is running and get public IP
ec2 = boto3.resource('ec2', region_name='us-east-1')
instance = ec2.Instance(instance_id)
print("Waiting for instance to be in 'running' state...")
instance.wait_until_running()
instance.load()
public_ip = instance.public_ip_address
print(f"Public IP: {public_ip}")

# Wait for Apache to finish loading
print("Waiting for Apache to start...")
time.sleep(30)

# Make a request to index.html
try:
    url = f"http://{public_ip}/index.html"
    response = requests.get(url)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Page Content:\n{response.text[:500]}...")
except Exception as e:
    print(f"Error calling the web page: {e}")
