import boto3
import json

# Create a Bedrock runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

prompt = "\n\nHuman: Tell me a fun fact about space.\n\nAssistant:"

response = bedrock_runtime.invoke_model(
    modelId='anthropic.claude-v2',
    contentType='application/json',
    accept='application/json',
    body=json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 300,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 0.999
    })
)

# Decode response
result = json.loads(response['body'].read())
print(result['completion'])
