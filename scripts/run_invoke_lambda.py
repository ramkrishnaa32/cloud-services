import boto3
import json

lambda_client = boto3.client('lambda')

event_payload = {
    "source_bucket": "cloud-services-preprod-us-east-1",
    "source_key": "candidate/candidate_details.csv",
    "destination_bucket": "de-testing-bucket-us-east-1",
    "destination_key": "staging/candidate_details.csv"
}

response = lambda_client.invoke(
    FunctionName="lambda-func-copy-object-s3",
    InvocationType="RequestResponse",
    Payload=json.dumps(event_payload),
)

print(json.load(response['Payload']))
