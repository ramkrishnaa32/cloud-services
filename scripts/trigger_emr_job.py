import boto3
import time

# Define your variables
application_id = '00fs78navnrucb09'
execution_role_arn = 'arn:aws:iam::650653607934:role/service-role/AmazonEMR-ExecutionRole-1746256001026'
script_path = 's3://cloud-services-preprod-us-east-1/serverless/script/application_orders.py'
data_path = 's3://cloud-services-preprod-us-east-1/serverless/data/'
output_path = 's3://cloud-services-preprod-us-east-1/serverless/output/'
log_path = 's3://cloud-services-preprod-us-east-1/serverless/logs/'

# Initialize EMR Serverless client
client = boto3.client('emr-serverless', region_name='us-east-1')

# Submit the job
response = client.start_job_run(
    applicationId=application_id,
    executionRoleArn=execution_role_arn,
    jobDriver={
        'sparkSubmit': {
            'entryPoint': script_path,
            'entryPointArguments': [data_path, output_path],
            'sparkSubmitParameters': '--conf spark.executor.memory=4G --conf spark.executor.cores=2'
        }
    },
    configurationOverrides={
        'monitoringConfiguration': {
            's3MonitoringConfiguration': {
                'logUri': log_path
            }
        }
    }
)

job_run_id = response['jobRunId']
print(f"Job submitted successfully!\nJobRunId: {job_run_id}")

# Monitor the job until completion
terminal_states = ['SUCCESS', 'FAILED', 'CANCELLED']
while True:
    job_status_response = client.get_job_run(
        applicationId=application_id,
        jobRunId=job_run_id
    )
    status = job_status_response['jobRun']['state']
    print(f"Job status: {status}")

    if status in terminal_states:
        if status == 'SUCCESS':
            print("Job completed successfully!")
        else:
            print(f"Job ended with status: {status}")
        break

    time.sleep(15)